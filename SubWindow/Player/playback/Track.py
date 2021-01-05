

class Track:
    def __init__(self, id_, language, description, bitrate=-1, codec=""):
        self.id = id_
        self.language = language if language != '' else "not set"
        self.description = description if description != '' else "not set"
        self.bitrate = bitrate
        self.codec = codec

    def __repr__(self):
        return f"[{self.language}] - {self.description}"
