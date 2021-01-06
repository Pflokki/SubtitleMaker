from SubWindow.Player.playback.Track import Track


class SubTrack(Track):
    def __init__(self, id_, language, description, *args, **kwargs):
        super(SubTrack, self).__init__(id_, language, description, *args, **kwargs)
