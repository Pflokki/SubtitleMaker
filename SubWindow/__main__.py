from PySide2.QtWidgets import QApplication
from SubWindow.Windows.MainWindow import MainWindow

import sys


class App(QApplication):
    def __init__(self):
        super(App, self).__init__()
        self.main_window = MainWindow()
        self.setActiveWindow(self.main_window)
        self.main_window.ui.show()


def run():
    app = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
