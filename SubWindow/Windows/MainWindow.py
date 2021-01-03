import os
from pathlib import Path

from PySide2.QtWidgets import QMainWindow, QFileDialog, QComboBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer, QEvent

from SubWindow.Windows.OnTopSubWindow import OnTopWindow
from SubWindow.Win32Helper import WindowList
from SubWindow.Player.Player import Player
from SubWindow.Subtitles import Subtitle

MAIN_WINDOW_PATH = r"Forms/form.ui"
MAIN_WINDOW_DIR = Path(__file__).parent.parent

WINDOW_TITLE = "VLC (Direct3D11 output)"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        path = Path.joinpath(MAIN_WINDOW_DIR, MAIN_WINDOW_PATH)
        self.ui = QUiLoader().load(os.path.join(path), self)  # !!! don't ask

        self.ui.pB_start.clicked.connect(self.play)

        self.video_path: Path = None
        self.ui.l_file_path.setText("Путь к видео: ")
        self.ui.pb_file_path.clicked.connect(self.open_video_dialog)
        self.ui.le_file_path.setText(r"M:\Cериалы\Doctor Who Series 12 (2020)\Doctor Who s12e01 Spyfall Part One.avi")

        self.sub_ext_path: Path = None
        self.ui.l_sub_ext.setText("Путь к субтитрам: ")
        self.ui.pb_sub_ext_path.clicked.connect(self.open_sub_ext_dialog)
        self.ui.le_sub_ext_path.setText(r"M:\Cериалы\Doctor Who Series 12 (2020)\Doctor Who s12e01 Spyfall Part One.eng.srt")

        self.ui.l_sound_track.setText("Аудио дорожка")
        self.ui.l_sub_track.setText("Субтитры")

        self.subtitle_window_position_timer = QTimer()
        self.subtitle_window_position_timer.setInterval(1)
        self.subtitle_window_position_timer.timeout.connect(self.create_sub_window)

        self.player = Player()

        self.windows = []
        self.window_list = WindowList()

        self.sub_window = OnTopWindow()
        self.subtitle = Subtitle()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.Enter:
            self.update_window_list()
            return True
        return False

    def create_sub_window(self):
        cur_time = self.player.get_current_time()
        if self.subtitle.is_changed(cur_time):
            self.sub_window.close()
            self.sub_window = OnTopWindow()
            self.sub_window.set_text(self.subtitle.get_subtitle(cur_time))
            self.sub_window.show()
        (x, y), (w, h) = self.window_list.get_window_rect(WINDOW_TITLE)
        self.sub_window.move(x + (w - x) / 2 - self.sub_window.width() / 2, h - self.sub_window.height())

    def open_video_dialog(self):
        # file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать файл")
        # self.ui.le_file_path.setText(file_name[0])
        self.video_path = Path(self.ui.le_file_path.text())

        self.load_file_info()

    def open_sub_ext_dialog(self):
        # file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать субтитры")
        # self.ui.pb_sub_ext_path.setText(file_name[0])
        self.sub_ext_path = Path(self.ui.le_sub_ext_path.text())

    def load_file_info(self):
        self.player.set_media(self.video_path)
        self.player.parse_meta()

        sound = self.player.get_sound_info()
        sub = self.player.get_sub_info()

        self.ui.cb_sound_track.clear()
        self.ui.cb_sound_track.addItems([str(track) for track in sound])
        self.ui.cb_sub_track.clear()
        self.ui.cb_sub_track.addItem("None")
        self.ui.cb_sub_track.addItems([str(track) for track in sub])

    def set_tracks(self, sub_id, soundtrack_id):
        if sub_id:
            self.player.set_sub(sub_id)
        self.player.set_sound(soundtrack_id)

    def play(self):
        # current_sub = self.player.get_sub_info()[self.ui.cb_sub_track.currentIndex() - 1].id \
        #     if self.ui.cb_sub_track.currentIndex() != 0 else None
        current_sub = None
        current_sound = self.player.get_sound_info()[self.ui.cb_sound_track.currentIndex()].id

        self.subtitle.open(self.sub_ext_path)

        self.player.play()
        while not self.player.started:  # used to delay before file will be opened
            pass
        self.set_tracks(current_sub, current_sound)  # must be sets after starting video

        self.subtitle_window_position_timer.start()
        # self.player.set_position_changed_handler(self.player_time_changed_handler)
        # while not self.player.is_stopped():
        #     self.subtitle_window.set_text("Hello World")
        #     self.subtitle_window.repaint()
