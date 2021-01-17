from PySide2.QtWidgets import QWidget, QVBoxLayout,  QMessageBox, QTableWidget, QTableWidgetItem
from PySide2.QtCore import Qt

WINDOW_TITLE = "Unknown words"


class WordWindow(QWidget):
    def __init__(self, parent=None):
        super(WordWindow, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)


class NewWordWidget(WordWindow):
    def __init__(self, parent=None):
        super(NewWordWidget, self).__init__(parent)

        self.table_widget = QTableWidget()
        self.table_widget.setGridStyle(Qt.DotLine)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("original"))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("translate"))
        self.table_widget.horizontalHeader().setDefaultSectionSize(250)
        self.table_widget.horizontalHeader().setMinimumSectionSize(100)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        self.main_layout.addWidget(self.table_widget)
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(530, 420)

    def set_content(self, dictionary: dict):
        self.table_widget.setRowCount(len(dictionary))
        for row_index, (word, translate) in enumerate(dictionary.items()):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(word))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(translate))


class NoNewWordMessageWindow(QWidget):
    def __init__(self, parent=None):
        super(NoNewWordMessageWindow, self).__init__(parent)

        text = "Поздравляю, при просмотре все слова оказались известными"
        self.message_box = QMessageBox()

        self.message_box.setWindowTitle(WINDOW_TITLE)
        self.message_box.setText(text)

    def show(self) -> None:
        self.message_box.show()