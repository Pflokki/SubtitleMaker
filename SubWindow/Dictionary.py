

class WordDictionary:
    def __init__(self):
        self.words = {

        }

    def get_translate(self, word: str):
        return self.words.get(word.lower(), None)

    def add(self, word: str, translate: str):
        if word.lower() not in self.words:
            self.words[word.lower()] = translate.lower()
