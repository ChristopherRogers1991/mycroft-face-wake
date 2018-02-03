from speech_recognition import Recognizer, AudioFile


class SimpleSTT(object):

    def __init__(self):
        self.recognizer = Recognizer()

    def transcribe(self, path_to_source):
        with AudioFile(path_to_source) as source:
            audio = self.recognizer.listen(source)
        return self.recognizer.recognize_google(audio)
