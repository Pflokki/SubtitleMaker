from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QWidgetItem
from PySide2.QtGui import QFont

from typing import List

from SubWindow.playback.ClickableLabel import ClickableLabel


class OnTopWindow(QWidget):
    def __init__(self):
        super(OnTopWindow, self).__init__()
        self.sub_labels: List[ClickableLabel] = []

        self.setWindowTitle("Sub")

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def get_main_layout_items(self) -> List[QWidgetItem]:
        return [self.main_layout.itemAt(index) for index in range(self.main_layout.count())]

    def clear_layout(self):
        for item in self.get_main_layout_items():
            self.main_layout.removeItem(item)
        self.sub_labels.clear()

    def update_labels_style(self):
        for label in self.sub_labels:
            label.setFont(QFont("Georgia", 28))
            label.setStyleSheet("color: red;")

    def add_label(self, sub_word: str):
        word_label = ClickableLabel(sub_word)
        self.main_layout.addWidget(word_label)
        self.sub_labels.append(word_label)

    def set_text(self, sub_string: str):
        self.clear_layout()
        words = sub_string.split(' ')
        for word in words:
            self.add_label(word)
        self.update_labels_style()
