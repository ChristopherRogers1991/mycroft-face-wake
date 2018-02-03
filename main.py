from object_watcher.object_watcher import ObjectWatcher
from simple_audio_recorder.simple_audio_recorder import SimpleAudioRecorder
import time

if __name__ == "__main__":
    recorder = SimpleAudioRecorder()

    with SimpleAudioRecorder() as recorder:
        fw = ObjectWatcher("./res/haarcascade_frontalface_default.xml", 0)
        fw.register_object_entered_callback(recorder.start_recording, "output.wav")
        fw.register_object_entered_callback(print, "recording!")
        fw.register_object_left_callback(recorder.stop_recording)
        fw.register_object_left_callback(print, "done recording!")

        fw.start()

        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            fw.terminate()
            fw.join()
