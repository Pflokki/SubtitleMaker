from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QKeyEvent

from pathlib import Path

from SubWindow.Player.Player import Player
from SubWindow.Windows.SubWidget import SubWidget
from SubWindow.Subtitles import Subtitle
from SubWindow.Translator import Translator
from SubWindow.Windows.WordWindow import NoNewWordMessageWindow, NewWordWidget

DEFAULT_WINDOW_TITLE = "SubPlayer"
DEFAULT_WINDOW_SIZE = (320, 240)


class PlayerWindow(QWidget):
    def __init__(self, parent=None):
        super(PlayerWindow, self).__init__(parent)

        self.setWindowTitle(DEFAULT_WINDOW_TITLE)

        self.player_frame = QFrame()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.player_frame)

        self.translator = Translator()
        self.sub_window = SubWidget(self.translator)
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
        elif event.key() in [Qt.Key_S, Qt.Key_Q]:
            self.end_video()
        elif event.key() == Qt.Key_T:
            self.player.toggle_time_showing()
        elif event.key() == Qt.Key_Up:
            self.player.volume_up()
        elif event.key() == Qt.Key_Down:
            self.player.volume_down()
        elif event.key() == Qt.Key_Left:
            self.player.step_backward()
        elif event.key() == Qt.Key_Right:
            self.player.step_forward()
        event.accept()

    def show_time_text(self):
        self.player.media_player.video_set_marquee_string()

    def end_video(self):
        self.subtitle_timer.stop()
        self.player.stop()
        self.resize(*DEFAULT_WINDOW_SIZE)
        self.sub_window.clear_layout()
        if len(self.translator.dictionary.words):
            self.table_word = NewWordWidget()
            self.table_word.set_content(self.translator.dictionary.words)
            self.table_word.show()
        else:
            self.msg_window = NoNewWordMessageWindow()
            self.msg_window.show()

    def show_full_screen(self):
        self.showMaximized()

    def show_normal_screen(self):
        self.showNormal()

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
        self.player.init_marque()

