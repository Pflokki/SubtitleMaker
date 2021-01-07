from PySide2.QtWidgets import QLabel
from re import compile
from SubWindow.Translator import Translator


class ClickableLabel(QLabel):
    def __init__(self, parent, translator: Translator):
        QLabel.__init__(self, parent)
        self.translator = translator

    def mousePressEvent(self, event):
        self.setStyleSheet("color: green;")
        self.setText(self.translate())

    def get_eng_text(self):
        return compile("[^a-zA-Z']").sub('', self.text())

    def translate(self):
        eng_text = self.get_eng_text()
        if len(eng_text) - eng_text.count("'"):
            return self.translator.translate(eng_text)
        else:
            return self.text()
