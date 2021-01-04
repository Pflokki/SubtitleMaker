from PySide2.QtWidgets import QWidget, QHBoxLayout, QFrame
from PySide2.QtCore import QTimer, QEvent, Qt
from PySide2.QtGui import QKeyEvent

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
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.player_frame)
        self.setLayout(self.main_layout)
        self.setMinimumSize(*DEFAULT_WINDOW_SIZE)

        self.player = Player()
        self.player.set_hwnd(self.player_frame.winId())

        self.update_sub_position_timer = QTimer()
        self.update_sub_position_timer.setInterval(1)
        self.update_sub_position_timer.timeout.connect(self.create_sub_window)

        self.sub_window = OnTopWindow()
        self.subtitle = Subtitle()

    def set_player_media(self, video_path: Path):
        self.setWindowTitle(f"{DEFAULT_WINDOW_TITLE} - {video_path.name}")
        self.player.set_media(video_path)
        self.player.parse_meta()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.player.toggle_play_pause()
        elif event.key() == Qt.Key_S:
            self.end_video()
        elif event.key() == Qt.Key_Q:
            self.player.stop()
            self.close()
        event.accept()

    def end_video(self):
        self.player.stop()
        self.resize(*DEFAULT_WINDOW_SIZE)

    def show_full_screen(self):
        self.showMaximized()

    def show_normal_screen(self):
        self.showNormal()

    def show(self) -> None:
        self.resize(*self.player.get_size())
        super().show()

    def create_sub_window(self):
        cur_time = self.player.get_current_time()
        if self.player.is_playing():
            if self.subtitle.is_changed(cur_time):
                self.sub_window.close()
                self.sub_window = OnTopWindow()
                self.sub_window.set_text(self.subtitle.get_subtitle(cur_time))
                self.sub_window.show()
                x, y = self.pos().x(), self.pos().y()
                w, h = self.width(), self.height()
                self.sub_window.move(x + w / 2 - self.sub_window.width() / 2, y + h - self.sub_window.height())
        else:
            self.end_video()

    def set_tracks(self, sub_id, soundtrack_id):
        if sub_id:
            self.player.set_sub(sub_id)
        self.player.set_sound(soundtrack_id)

    def play(self, sound_id, sub_id, sub_ext_path):
        current_sound = self.player.get_sound_info()[sound_id].id
        current_sub = None
        if sub_ext_path:
            self.subtitle.open(sub_ext_path)
        elif sub_id != 0:
            current_sub = self.player.get_sub_info()[sub_id - 1].id

        self.player.play()
        while not self.player.started:  # used to delay before file will be opened
            pass
        self.set_tracks(current_sub, current_sound)  # must be sets after starting video

        if sub_ext_path:
            self.update_sub_position_timer.start()
