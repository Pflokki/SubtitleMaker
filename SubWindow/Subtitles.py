from pathlib import Path
from pysrt import SubRipFile, open as pysrt_open, SubRipItem


class Subtitle:
    def __init__(self):
        self.path: Path = None
        self.sub_track: SubRipFile = None

        self.current_sub_item: SubRipItem = None

    def open(self, path: Path):
        self.path: Path = path
        self.sub_track: SubRipFile = pysrt_open(self.path.as_posix())

        self.current_sub_item: SubRipItem = None

    def is_changed(self, time):
        return self.current_sub_item is None or self.current_sub_item != self._get_sub_item(time)

    def get_subtitle(self, time):
        self.current_sub_item = self._get_sub_item(time)
        return self.current_sub_item.text

    def _get_sub_item(self, time):
        track = self.sub_track.at(time)
        return track
