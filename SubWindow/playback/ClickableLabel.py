from PySide2.QtWidgets import QLabel
from SubWindow.Translator import Translator
from SubWindow.playback.TextSplitter import TextSplitter


class ClickableLabel(QLabel):
    def __init__(self, parent, translator: Translator):
        QLabel.__init__(self, parent)
        self.translator = translator

        self.source_text = None
        self.translated_text = None

    def mousePressEvent(self, event):
        self.setStyleSheet("color: green;")
        if not self.source_text:
            self.translate()
        if self.source_text == self.text():
            self.setText(self.translated_text)
        else:
            self.setText(self.source_text)

    def translate(self):
        if not self.translated_text:
            self.source_text = self.text()
            splitter = TextSplitter(self.source_text)
            if splitter.text:
                translated_text = self.translator.translate(splitter.text)
                self.translated_text = splitter.replace_text(translated_text)
