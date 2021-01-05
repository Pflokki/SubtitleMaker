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

    def update_tracks_info(self):
        self.tracks.clear()
        tracks = ffmpeg.probe(self.path).get('streams', [])

        for track in tracks:
            codec_type = track.get('codec_type', "other")

            index = track.get('index', -1)
            t_desc = track.get('tags', {})
            language = t_desc.get('language', "not set")
            description = t_desc.get('title', "not set")
            bitrate = int(track.get('bit_rate', -1))
            codec = track.get('codec_long_name', -1)

            self.tracks.append(CODEC_TYPE_HANDLER[codec_type](index, language, description, bitrate, codec))

    def get_video_track_list(self):
        return [track for track in self.tracks if isinstance(track, VideoTrack)]

    def get_audio_track_list(self):
        return [track for track in self.tracks if isinstance(track, AudioTrack)]

    def get_sub_track_list(self):
        return [track for track in self.tracks if isinstance(track, SubTrack)]
