from pathlib import Path
import ffmpeg

from SubWindow.Player.playback.VideoTrack import VideoTrack
from SubWindow.Player.playback.AudioTrack import AudioTrack
from SubWindow.Player.playback.SubTrack import SubTrack
from SubWindow.Player.playback.SubTrack import Track


CODEC_TYPE_HANDLER = {
    'video': VideoTrack,
    'audio': AudioTrack,
    'subtitle': SubTrack,
    'other': Track,

}


class Video:
    def __init__(self):
        self.path: Path = Path()

        self.tracks = []

    def set_path(self, path: str):
        self.path = Path(path)

    @property
    def name(self):
        return self.path.name

    @property
    def video_size(self):
        return self.get_video_track_list()[0].video_size

    def update_tracks_info(self):
        self.tracks.clear()
        tracks = ffmpeg.probe(self.path).get('streams', [])

        for track in tracks:
            codec_type = track.get('codec_type', "other")

            t_desc = track.get('tags', {})
            index = track.get('index', -1)
            language = t_desc.get('language', "not set")
            description = t_desc.get('title', "not set")
            kwargs = {
                'bitrate': int(track.get('bit_rate', -1)),
                'codec': track.get('codec_long_name', -1),
                'video_size': (track.get('width', 320), track.get('height', 240)),
            }
            self.tracks.append(CODEC_TYPE_HANDLER[codec_type](index, language, description, **kwargs))

    def get_video_track_list(self):
        return [track for track in self.tracks if isinstance(track, VideoTrack)]

    def get_audio_track_list(self):
        return [track for track in self.tracks if isinstance(track, AudioTrack)]

    def get_sub_track_list(self):
        return [track for track in self.tracks if isinstance(track, SubTrack)]

    def get_subtitle(self, sub_index):
        sub_path = self.path.parent.joinpath(self.path.name.replace(self.path.suffix, f'_sub_{sub_index}.srt'))
        infile = ffmpeg.input(self.path.as_posix())
        outfile = ffmpeg.output(infile[f'{sub_index}'], sub_path.as_posix(), codec='copy')
        ffmpeg.run(outfile, overwrite_output=True)
        return sub_path
