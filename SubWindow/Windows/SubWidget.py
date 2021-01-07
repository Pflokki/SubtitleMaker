from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QWidgetItem, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
from PySide2.QtGui import QFont

from typing import List

from SubWindow.playback.ClickableLabel import ClickableLabel


class SubWidget(QWidget):
    def __init__(self, translator):
        super(SubWidget, self).__init__()
        self.sub_labels: List[ClickableLabel] = []

        self.setStyleSheet("background:transparent;")

        self.main_layout = QHBoxLayout()
        self.sub_layout = QHBoxLayout()

        left_spacer = QSpacerItem(2000, 1, QSizePolicy.Maximum, QSizePolicy.Expanding)
        right_spacer = QSpacerItem(2000, 1, QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.main_layout.addSpacerItem(left_spacer)
        self.main_layout.addLayout(self.sub_layout)
        self.main_layout.addSpacerItem(right_spacer)

        self.setLayout(self.main_layout)

        self.translator = translator

    def get_sub_layout_items(self) -> List[QWidgetItem]:
        return [self.sub_layout.itemAt(index) for index in range(self.sub_layout.count())]

    def clear_layout(self):
        for item in reversed(range(self.sub_layout.count())):
            self.sub_layout.itemAt(item).widget().setParent(None)

    def update_labels_style(self):
        effect = QGraphicsDropShadowEffect()
        effect.setColor(Qt.black)
        effect.setOffset(-1, -1)
        for label in self.sub_labels:
            label.setFont(QFont("Georgia", 22))
            label.setStyleSheet("color: black;")
            label.setGraphicsEffect(effect)

    def add_label(self, sub_word: str):
        word_label = ClickableLabel(sub_word, self.translator)
        self.sub_layout.addWidget(word_label)
        self.sub_labels.append(word_label)

    def set_text(self, sub_string: str):
        self.clear_layout()
        words = sub_string.split(' ')
        for word in words:
            self.add_label(word)
        self.update_labels_style()
