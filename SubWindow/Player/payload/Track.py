

class Track:
    def __init__(self, id_, language, description, *args, **kwargs):
        self.id = id_
        self.language = language if language != '' else "not set"
        self.description = description if description != '' else "not set"
        self.bitrate = kwargs.get('bitrate', -1)
        self.codec = kwargs.get('codec', "")

    def __repr__(self):
        return f"[{self.language}] - {self.description}"
