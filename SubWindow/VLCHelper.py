from vlc import Instance, MediaPlayer


class VLCHelper:
    def __init__(self, path):
        self.instance: Instance = Instance()
        self.player: MediaPlayer = self.instance.media_player_new(path)
        self.player.play()
