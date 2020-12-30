import os
from pathlib import Path

from PySide2.QtWidgets import QMainWindow, QComboBox, QLabel, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer, QEvent

from SubWindow.Windows.OnTopSubWindow import OnTopWindow
from SubWindow.Win32Helper import WindowList
from SubWindow.VLCHelper import VLCHelper

MAIN_WINDOW_PATH = r"Forms/form.ui"
MAIN_WINDOW_DIR = Path(__file__).parent.parent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windows = []
        self.window_list = WindowList()

        path = Path.joinpath(MAIN_WINDOW_DIR, MAIN_WINDOW_PATH)
        self.ui = QUiLoader().load(os.path.join(path), self)  # !!! don't ask

        self.ui.pB_start.clicked.connect(self.create_subtitle_window)
        self.ui.cB_window.installEventFilter(self)

        self.file_path = Path()
        self.ui.l_file_path.setText("Путь к видео: ")
        self.ui.pb_file_path.setText("...")
        self.ui.pb_file_path.clicked.connect(self.open_file_dialog)

        self.subtitle_window = OnTopWindow()
        self.subtitle_window_position_timer = QTimer()
        self.subtitle_window_position_timer.setInterval(0)
        self.subtitle_window_position_timer.timeout.connect(self.move_subtitle_window)
        self.update_window_list()

    def update_window_list(self):
        current_text = self.ui.cB_window.currentText()
        self.window_list.update()
        self.ui.cB_window.clear()
        self.ui.cB_window.addItems(self.window_list.titles)
        index = self.window_list.get_index(current_text)
        if index:
            self.ui.cB_window.setCurrentIndex(index)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.Enter:
            self.update_window_list()
            return True
        return False

    def get_chosen_window_position(self):
        item_index = self.ui.cB_window.currentIndex()
        _, window = self.window_list.at(item_index)
        (x, y), (w, h) = self.window_list.get_window_rect(window)
        return (x, y), (w, h)

    def move_subtitle_window(self):
        (x, y), (w, h) = self.get_chosen_window_position()
        self.subtitle_window.move(x + (w - x) / 2 - self.subtitle_window.width() / 2, h - self.subtitle_window.height())

    def open_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.ui, "Открыть файл")
        self.file_path = Path(file_name[0])
        self.ui.le_file_path.setText(file_name[0])

    def create_subtitle_window(self):
        if self.file_path:
            vlc = VLCHelper(self.file_path)

            self.subtitle_window.set_text("Hello World, it's me, Mario")
            self.subtitle_window_position_timer.start()
            self.subtitle_window.show()

