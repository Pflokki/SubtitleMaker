from PySide2.QtWidgets import QLabel


class ClickableLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, event):
        # open the link on your browser
        self.setStyleSheet("color: green;")
