from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide2.QtCore import QTimer, QEvent, Qt
from PySide2.QtGui import QKeyEvent, QMoveEvent

from pathlib import Path

from SubWindow.Player.Player import Player
from SubWindow.Windows.OnTopSubWindow import OnTopWindow
from SubWindow.Subtitles import Subtitle

DEFAULT_WINDOW_TITLE = "SubPlayer"
DEFAULT_WINDOW_SIZE = (320, 240)


class PlayerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(DEFAULT_WINDOW_TITLE)

        self.player_frame = QFrame()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.player_frame)

        self.sub_window = OnTopWindow()
        self.main_layout.addWidget(self.sub_window)

        self.main_layout.setStretchFactor(self.player_frame, 100)
        self.main_layout.setStretchFactor(self.sub_window, 1)

        self.setLayout(self.main_layout)
        self.setMinimumSize(*DEFAULT_WINDOW_SIZE)

        self.player = Player()
        self.player.set_hwnd(self.player_frame.winId())

        self.subtitle_timer = QTimer()
        self.subtitle_timer.setInterval(1)
        self.subtitle_timer.timeout.connect(self.update_subtitles)

        self.subtitle = Subtitle()

    def set_player_media(self, video_path: Path):
        self.setWindowTitle(f"{DEFAULT_WINDOW_TITLE} - {video_path.name}")
        self.player.set_media(video_path)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.player.toggle_play_pause()
        elif event.key() == Qt.Key_S:
            self.end_video()
            self.sub_window.clear_layout()
        elif event.key() == Qt.Key_Q:
            self.player.stop()
            self.close()
        event.accept()

    # def set_subtitle_widget_position(self):
    #     x, y = self.pos().x(), self.pos().y()
    #     w, h = self.width(), self.height()
    #     self.sub_window.move(x + w / 2 - self.sub_window.width() / 2, y + h - self.sub_window.height())

    def end_video(self):
        self.player.stop()
        self.resize(*DEFAULT_WINDOW_SIZE)

    def show_full_screen(self):
        self.showMaximized()

    def show_normal_screen(self):
        self.showNormal()

    def show(self) -> None:
        super().show()

    def resize_window(self, window_size: tuple):
        self.resize(*window_size)

    def update_subtitles(self):
        cur_time = self.player.get_current_time()
        if self.player.is_playing():
            if self.subtitle.is_changed(cur_time):
                self.sub_window.set_text(self.subtitle.get_subtitle(cur_time))
        elif self.player.is_stopped():
            self.end_video()

    def set_tracks(self, soundtrack_id):
        self.player.set_sound(soundtrack_id)
        self.player.disable_sub()

    def play(self, sound_id, sub_path):
        if sub_path:
            self.subtitle.open(sub_path)
            self.subtitle_timer.start()

        self.player.play()
        while not self.player.started:  # used to delay before file will be opened
            pass
        self.set_tracks(sound_id)  # must be sets after starting video
