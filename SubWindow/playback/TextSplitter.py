from re import compile


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
