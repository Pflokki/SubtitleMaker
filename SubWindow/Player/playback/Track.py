

class Track:
    def __init__(self, id_, language, description, bitrate=-1, codec=-1):
        self.id = id_
        self.language = language
        self.description = description
        self.bitrate = bitrate
        self.codec = codec

    def __repr__(self):
        return f"[{self.language}] - {self.description}"
