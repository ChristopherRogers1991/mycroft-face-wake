import pyaudio
import wave
from threading import Thread
import logging


log = logging.getLogger(__name__)

class SimpleAudioRecorder(object):

    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100,
                 frames_per_buffer=1024):
        """
        All parameters are passed straight to an instance of pyaudio.PyAudio

        Parameters
        ----------
        format : int
        channels : int
        rate : int
        frames_per_buffer : int
        """
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.thread = None
        self._stop_recording = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def start_recording(self, destination):
        """
        Call this to begin recording audio. Audio recording will be done in a
        separate thread. Call `stop_recording` to stop the recording, and write
        the resulting audio to `destination`.

        Calling multiple times before calling `stop_recording` will have no
        effect (other than a logged warning).

        Parameters
        ----------
        destination : str
            Path to an output file. If it does not exist, it will be created.
            If is does exist, it will be overwritten.

        """
        if self.recording:
            log.warning("Already recording!")
            return

        self.thread = Thread(target=self._record_until_stopped,
                             args=[destination])
        self.thread.start()

    def _record_until_stopped(self, destination):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                 frames_per_buffer=self.frames_per_buffer)

        frames = []
        while not self._stop_recording:
            data = stream.read(self.frames_per_buffer)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self._write_wave_file(frames, destination)

    def _write_wave_file(self, frames, destination):
        waveFile = wave.open(destination, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def stop_recording(self):
        self._stop_recording = True
        self.thread.join()
        self.recording = False
        self._stop_recording = False

    def terminate(self):
        """

        Wraps `self.audio.terminate`. See PyAudio docs
        for details.

        """
        self.audio.terminate()


if __name__ == "__main__":
    import time
    recorder = SimpleAudioRecorder()
    recorder.start_recording("./test.wav")
    time.sleep(5)
    recorder.stop_recording()
