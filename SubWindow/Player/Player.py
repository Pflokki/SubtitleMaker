from vlc import Instance, MediaPlayer, Media, EventType, EventManager, VideoMarqueeOption
import datetime


class Player:
    def __init__(self):
        self.instance: Instance = Instance()
        self.media_player: MediaPlayer = self.instance.media_player_new()

        self.media: Media = None

        self.started = False
        self.stopped = False
        self.is_show_time = False
        self.event_manager: EventManager = self.media_player.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.player_position_changed)
        self.event_manager.event_attach(EventType.MediaPlayerStopped, self.player_stopped)

    def init_marque(self):
        self.media_player.video_set_marquee_int(VideoMarqueeOption.Enable, 1)
        self.media_player.video_set_marquee_int(VideoMarqueeOption.Size, 36)  # pixels

    def toggle_play_pause(self):
        if self.is_playing():
            self.pause()
            self.media_player.video_set_marquee_string(VideoMarqueeOption.Text, "Пауза")
            self.media_player.video_set_marquee_int(VideoMarqueeOption.Timeout, 1000)
        elif self.started:
            self.play()
            self.media_player.video_set_marquee_string(VideoMarqueeOption.Text, "Воспроизведение")
            self.media_player.video_set_marquee_int(VideoMarqueeOption.Timeout, 1000)

    def toggle_time_showing(self):
        self.is_show_time = not self.is_show_time

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
        if self.is_show_time:
            self.media_player.video_set_marquee_string(VideoMarqueeOption.Text, self.get_formatted_time())
            self.media_player.video_set_marquee_int(VideoMarqueeOption.Timeout, 1000)

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def volume_up(self):
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(min(volume + 10, 100))
        self.show_volume_text()

    def volume_down(self):
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(max(volume - 10, 0))
        self.show_volume_text()

    def step_forward(self):
        f_time = self.get_current_time()
        self.media_player.set_time(min(f_time + 10 * 1000, self.media_player.get_length()))

    def step_backward(self):
        b_time = self.get_current_time()
        self.media_player.set_time(max(b_time - 10 * 1000, 0))

    def is_playing(self):
        return bool(self.media_player.is_playing())

    def is_stopped(self):
        return self.started and self.stopped

    def player_stopped(self, *args, **kwargs):
        self.stopped = True

    def show_volume_text(self):
        volume = self.get_formatted_volume()
        self.media_player.video_set_marquee_string(VideoMarqueeOption.Text, volume)
        self.media_player.video_set_marquee_int(VideoMarqueeOption.Timeout, 500)

    def get_current_time(self):
        return self.media_player.get_time()

    def get_formatted_time(self):
        time_format = "%H:%M:%S"
        current_time = datetime.datetime.utcfromtimestamp(self.media_player.get_time() / 1000.0)
        length = datetime.datetime.utcfromtimestamp(self.media_player.get_length() / 1000.0)

        return f"{current_time.strftime(time_format)} / {length.strftime(time_format)}"

    def get_formatted_volume(self):
        return f"Громкость: {self.media_player.audio_get_volume()}"
