from PySide2.QtWidgets import QApplication
from SubWindow.Windows.MainWindow import MainWindow

import sys


def run():
    main_event_thread = QApplication()
    application = MainWindow()
    application.ui.show()
    sys.exit(main_event_thread.exec_())


if __name__ == '__main__':
    run()
