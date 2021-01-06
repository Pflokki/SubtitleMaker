from SubWindow.Player.playback.Track import Track


class AudioTrack(Track):
    def __init__(self, id_, language, description, *args, **kwargs):
        super(AudioTrack, self).__init__(id_, language, description, *args, **kwargs)
