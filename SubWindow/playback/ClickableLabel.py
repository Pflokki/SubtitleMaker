from PySide2.QtWidgets import QLabel
from re import compile
from SubWindow.Translator import Translator


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

    def get_text(self):
        return compile("([^a-zA-Z]*)([a-zA-Z']+)([^a-zA-Z]*)").split(self.text())

    def translate(self):
        if not self.translated_text:
            self.source_text = self.text()
            splitter = TextSplitter(self.source_text)
            if splitter.text:
                translated_text = self.translator.translate(splitter.text)
                self.translated_text = splitter.replace_text(translated_text)


class TextSplitter:
    def __init__(self, text):
        self.raw_text = text
        self.prefix = None
        self.text = None
        self.postfix = None

        self.split()

    @property
    def f_text(self):
        return f"{self.prefix}{self.text}{self.postfix}"

    def split(self):
        text = compile("([^a-zA-Z]*)([a-zA-Z']+)([^a-zA-Z]*)").split(self.raw_text)
        if len(text) >= 3:
            self.prefix, self.text, self.postfix = text[1:-1]

    def replace_text(self, text):
        self.text = text
        return self.f_text
