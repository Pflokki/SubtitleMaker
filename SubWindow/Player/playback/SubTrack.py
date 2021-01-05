from SubWindow.Player.playback.Track import Track


class SubTrack(Track):
    def __init__(self, id_, language, description, bitrate, codec):
        super(SubTrack, self).__init__(id_, language, description, bitrate, codec)
