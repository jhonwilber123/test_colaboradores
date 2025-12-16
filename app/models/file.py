
class File:
    
    def __init__(self, filename: str, transcription: str):
        self.filename = filename
        self.transcription = transcription


class AudioFile(File):
    
    def __init__(self, filename: str, transcription: str):
        super().__init__(filename, transcription)