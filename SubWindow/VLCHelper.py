from vlc import Instance, MediaPlayer, Event, EventType, libvlc_add_intf, EventManager, VideoMarqueeOption, Position, str_to_bytes


class VLCHelper:
    def __init__(self, path):
        self.instance: Instance = Instance(["--sub-source=marq"])
        self.player: MediaPlayer = self.instance.media_player_new(path)
        self.started = False

        self.event_manager: EventManager = self.player.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.player_position_changed)
        self.player.video_set_key_input(True)

    def player_position_changed(self, *args, **kwargs):
        self.started = True
        print(f"time: {self.get_current_time()}")

    def play(self):
        self.player.play()

    def get_current_time(self):
        return self.player.get_time()

    def test(self):
        self.player.get_xwindow()

    def get_sound_info(self):
        track = self.player.video_get_track()
        count = self.player.video_get_track_count()
        desc = self.player.video_get_track_description()
        pass

    def get_sub_info(self):
        spu = self.player.video_get_spu()
        count = self.player.video_get_spu_count()
        desc = self.player.video_get_spu_description()
        pass