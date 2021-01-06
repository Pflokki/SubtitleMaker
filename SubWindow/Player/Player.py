from vlc import Instance, MediaPlayer, Media, EventType, EventManager, TrackType


class Player:
    def __init__(self):
        self.instance: Instance = Instance()
        self.media_player: MediaPlayer = self.instance.media_player_new()

        self.media: Media = None

        self.started = False
        self.stopped = False
        self.event_manager: EventManager = self.media_player.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.player_position_changed)
        self.event_manager.event_attach(EventType.MediaPlayerStopped, self.player_stopped)

        # self.pos_changed_handler = None

    def toggle_play_pause(self):
        if self.is_playing():
            self.pause()
        elif self.started:
            self.play()

    def set_hwnd(self, hwnd):
        self.media_player.set_hwnd(hwnd)

    def get_hwnd(self):
        return self.media_player.get_hwnd()

    # def set_position_changed_handler(self, handler: callable):
    #     self.pos_changed_handler = handler

    def set_media(self, path):
        self.media: Media = self.instance.media_new(path)
        self.media_player.set_media(self.media)

    def disable_sub(self):
        return self.media_player.video_set_spu(-1)

    def set_sound(self, soundtrack_id: int):
        return self.media_player.audio_set_track(soundtrack_id)

    def player_position_changed(self, *args, **kwargs):
        self.started = True
        # if self.pos_changed_handler is not None:
        #     self.pos_changed_handler(self.get_current_time())

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def volume_up(self):
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(min(volume + 10, 100))

    def volume_down(self):
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(max(volume - 10, 0))

    def step_forward(self):
        time = self.get_current_time()
        self.media_player.set_time(min(time + 10 * 1000, self.media_player.get_length()))

    def step_backward(self):
        time = self.get_current_time()
        self.media_player.set_time(max(time - 10 * 1000, 0))

    def is_playing(self):
        return bool(self.media_player.is_playing())

    def is_stopped(self):
        return self.started and self.stopped

    def player_stopped(self, *args, **kwargs):
        self.stopped = True

    def get_current_time(self):
        return self.media_player.get_time()
