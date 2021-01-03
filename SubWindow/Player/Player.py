from SubWindow.Player.playback.VideoTrack import VideoTrack
from SubWindow.Player.playback.AudioTrack import AudioTrack
from SubWindow.Player.playback.SubTrack import SubTrack

from vlc import Instance, MediaPlayer, Media, EventType, EventManager, TrackType


class Player:
    def __init__(self):
        self.instance: Instance = Instance()
        self.media_player: MediaPlayer = self.instance.media_player_new()

        self.media: Media = None
        self.tracks = []

        self.started = False
        self.event_manager: EventManager = self.media_player.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.player_position_changed)

    def set_media(self, path):
        self.media: Media = self.instance.media_new(path)
        self.media_player.set_media(self.media)

    def set_sub(self, track_id: int):
        return self.media_player.video_set_spu(track_id)

    def set_sound(self, soundtrack_id: int):
        return self.media_player.audio_set_track(soundtrack_id)

    def parse_meta(self):
        self.media.parse()
        self.tracks = list(self.media.tracks_get())

    def player_position_changed(self, *args, **kwargs):
        self.started = True
        print(f"time: {self.get_current_time()}")

    def play(self):
        self.media_player.play()

    def get_current_time(self):
        return self.media_player.get_time()

    def test(self):
        self.media_player.get_xwindow()

    def __get_param_from_track(self, track):
        return track.id, \
               track.language.decode("utf-8") if track.language else "", \
               track.description.decode("utf-8") if track.description else "", \
               track.bitrate, \
               track.codec

    def get_sound_info(self):
        return [AudioTrack(*self.__get_param_from_track(track))
                for track in self.tracks if track.type == TrackType.audio]

    def get_sub_info(self):
        return [SubTrack(*self.__get_param_from_track(track)[:-2])
                for track in self.tracks if track.type == TrackType.ext]

    def get_video_info(self):
        return [VideoTrack(*self.__get_param_from_track(track))
                for track in self.tracks if track.type == TrackType.video]
