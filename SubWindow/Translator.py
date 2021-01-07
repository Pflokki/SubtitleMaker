import json
import requests
import configparser
from pathlib import Path

from SubWindow.Dictionary import WordDictionary


class Translator:
    def __init__(self):
        self.dictionary = WordDictionary()

        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.joinpath('settings.ini'))
        api_key = config['API KEYS']['rapidapi-key']

        self.url = "https://microsoft-translator-text.p.rapidapi.com/translate"
        self.querystring = {"to": "ru", "api-version": "3.0"}
        self.headers = {
            "content-type": "application/json",
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
        }

    def translate(self, sentence: str):
        translate = self.dictionary.get_translate(sentence)
        if not translate:
            payload = json.dumps([{'text': f"{sentence}"}])

            response = requests.request("POST", self.url, data=payload, headers=self.headers, params=self.querystring)
            translations = json.loads(response.text)[0].get('translations', [])
            translate: str = translations[0].get('text', "").lower()
            self.dictionary.add(sentence, translate)
        return translate
