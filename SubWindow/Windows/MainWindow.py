import os
from pathlib import Path

from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtUiTools import QUiLoader

from SubWindow.Windows.PlayerWindow import PlayerWindow

from SubWindow.Video import Video

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

        self.ui.l_sub_ext.setText("Путь к субтитрам: ")
        self.ui.pb_sub_ext_path.clicked.connect(self.open_sub_ext_dialog)

        self.ui.l_sound_track.setText("Аудио дорожка")
        self.ui.l_sub_track.setText("Субтитры")

        self.player_window = PlayerWindow()
        self.video = Video()

    def open_video_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать файл")
        self.ui.le_file_path.setText(file_name[0])
        if file_name:
            self.video.set_path(file_name[0])
            self.load_file_info()

    def open_sub_ext_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Выбрать субтитры")
        self.ui.le_sub_ext_path.setText(file_name[0])

    def load_file_info(self):
        vide_file_path = Path(self.ui.le_file_path.text())
        self.player_window.set_player_media(vide_file_path)

        self.video.update_tracks_info()

        sound = self.video.get_audio_track_list()
        sub = self.video.get_sub_track_list()

        self.ui.cb_sound_track.clear()
        self.ui.cb_sound_track.addItems([str(track) for track in sound])
        self.ui.cb_sub_track.clear()
        self.ui.cb_sub_track.addItem("None")
        self.ui.cb_sub_track.addItems([str(track) for track in sub])
        pass

    def play(self):
        self.player_window.resize_window(self.video.video_size)
        self.player_window.show()
        audio_id = self.video.get_audio_track_list()[self.ui.cb_sound_track.currentIndex()].id
        if self.ui.le_sub_ext_path.text():
            sub_ext_path = Path(self.ui.le_sub_ext_path.text())
        elif self.ui.cb_sub_track.currentIndex() != 0:
            sub_id = self.video.get_sub_track_list()[self.ui.cb_sub_track.currentIndex() - 1].id
            sub_ext_path = self.video.get_subtitle(sub_id)
        else:
            sub_ext_path = None
        self.player_window.play(audio_id, sub_ext_path)
