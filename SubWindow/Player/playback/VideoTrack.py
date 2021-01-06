from SubWindow.Player.playback.Track import Track


class VideoTrack(Track):
    def __init__(self, id_, language, description, *args, **kwargs):
        super(VideoTrack, self).__init__(id_, language, description, *args, **kwargs)

        self.video_size = kwargs.get("video_size")
