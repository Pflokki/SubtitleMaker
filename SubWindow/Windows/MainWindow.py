import os
from pathlib import Path

from PySide2.QtWidgets import QMainWindow, QFileDialog, QComboBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer, QEvent

from SubWindow.Windows.OnTopSubWindow import OnTopWindow
from SubWindow.Win32Helper import WindowList
from SubWindow.Player.Player import Player

MAIN_WINDOW_PATH = r"Forms/form.ui"
MAIN_WINDOW_DIR = Path(__file__).parent.parent

WINDOW_TITLE = "VLC (Direct3D11 output)"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        path = Path.joinpath(MAIN_WINDOW_DIR, MAIN_WINDOW_PATH)
        self.ui = QUiLoader().load(os.path.join(path), self)  # !!! don't ask

        self.ui.pB_start.clicked.connect(self.play)

        self.file_path: Path = None
        self.ui.l_file_path.setText("Путь к видео: ")
        self.ui.pb_file_path.setText("...")
        self.ui.pb_file_path.clicked.connect(self.open_file_dialog)
        self.ui.le_file_path.setText(r"M:/Cериалы/Californication/Californication.S03.720p.WEB-DL.2xRus.Eng.HDCLUB/Californication.S03E01.720p.WEB-DL.2xRus.Eng.HDCLUB.mkv")

        self.ui.l_sound_track.setText("Аудио дорожка")
        self.ui.l_sub_track.setText("Субтитры")

        self.subtitle_window = OnTopWindow()
        self.subtitle_window_position_timer = QTimer()
        self.subtitle_window_position_timer.setInterval(0)
        self.subtitle_window_position_timer.timeout.connect(self.move_subtitle_window)

        self.player = Player()

        self.windows = []
        self.window_list = WindowList()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.Enter:
            self.update_window_list()
            return True
        return False

    def move_subtitle_window(self):
        (x, y), (w, h) = self.window_list.get_window_rect(WINDOW_TITLE)
        self.subtitle_window.move(x + (w - x) / 2 - self.subtitle_window.width() / 2, h - self.subtitle_window.height())

    def open_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Открыть файл")
        self.file_path = Path(file_name[0])
        self.ui.le_file_path.setText(file_name[0])

        self.load_file_info()

    def load_file_info(self):
        path = self.file_path if self.file_path else self.ui.le_file_path.text()
        self.player.set_media(path)
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
        current_sub = self.player.get_sub_info()[self.ui.cb_sub_track.currentIndex() - 1].id \
            if self.ui.cb_sub_track.currentIndex() != 0 else None
        current_sound = self.player.get_sound_info()[self.ui.cb_sound_track.currentIndex()].id

        self.player.play()
        while not self.player.started:
            pass
        self.set_tracks(current_sub, current_sound)  # must be sets after starting video

        self.subtitle_window_position_timer.start()
        self.subtitle_window.set_text("Hello World, it's me, Mario")
        self.subtitle_window.show()

