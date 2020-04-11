

class Sbb: #SoundBoardBot
    queue = []
    is_playing = False
    is_connected = False
    caller_name = ""
    chanel_mame = None
    voice_channel = None

    def __init__(self, caller_name):
        self.caller_name = caller_name
