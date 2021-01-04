import os
from pathlib import Path

from PySide2.QtWidgets import QMainWindow, QFileDialog, QComboBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QEvent

from SubWindow.Windows.PlayerWindow import PlayerWindow
from SubWindow.Win32Helper import WindowList

MAIN_WINDOW_PATH = r"Forms/form.ui"
MAIN_WINDOW_DIR = Path(__file__).parent.parent



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        path = Path.joinpath(MAIN_WINDOW_DIR, MAIN_WINDOW_PATH)
        self.ui = QUiLoader().load(os.path.join(path), self)  # !!! don't ask

        self.ui.pB_start.clicked.connect(self.play)

        self.ui.l_file_path.setText("Путь к видео: ")
        self.ui.pb_file_path.clicked.connect(self.open_video_dialog)
        self.ui.le_file_path.setText(r"M:\Cериалы\Doctor Who Series 12 (2020)\Doctor Who s12e01 Spyfall Part One.avi")

        self.ui.l_sub_ext.setText("Путь к субтитрам: ")
        self.ui.pb_sub_ext_path.clicked.connect(self.open_sub_ext_dialog)
        self.ui.le_sub_ext_path.setText(r"M:\Cериалы\Doctor Who Series 12 (2020)\Doctor Who s12e01 Spyfall Part One.eng.srt")

        self.ui.l_sound_track.setText("Аудио дорожка")
        self.ui.l_sub_track.setText("Субтитры")

        self.player_window = PlayerWindow()

        self.windows = []
        self.window_list = WindowList()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.Enter:
            self.update_window_list()
            return True
        return False

    def open_video_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать файл")
        self.ui.le_file_path.setText(file_name[0])
        if file_name:
            self.load_file_info()

    def open_sub_ext_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать субтитры")
        self.ui.le_sub_ext_path.setText(file_name[0])

    def load_file_info(self):
        self.player_window.set_player_media(Path(self.ui.le_file_path.text()))

        sound = self.player_window.player.get_sound_info()
        sub = self.player_window.player.get_sub_info()

        self.ui.cb_sound_track.clear()
        self.ui.cb_sound_track.addItems([str(track) for track in sound])
        self.ui.cb_sub_track.clear()
        self.ui.cb_sub_track.addItem("None")
        self.ui.cb_sub_track.addItems([str(track) for track in sub])

    def play(self):
        sub_ext_path = Path(self.ui.le_sub_ext_path.text()) if self.ui.le_sub_ext_path.text() else None
        self.player_window.show()
        self.player_window.play(self.ui.cb_sound_track.currentIndex(), self.ui.cb_sub_track.currentIndex(),
                                sub_ext_path)
