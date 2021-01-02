from SubWindow.Player.playback.Track import Track


class VideoTrack(Track):
    def __init__(self, id_, language, description, bitrate, codec):
        super(VideoTrack, self).__init__(id_, language, description, bitrate, codec)
