from object_watcher.object_watcher import ObjectWatcher
from simple_audio_recorder.simple_audio_recorder import SimpleAudioRecorder
from stt.simple_stt import SimpleSTT
import time
import traceback

transcriber = SimpleSTT()


def transcribe_and_print(path_to_source):
    try:
        text = transcriber.transcribe(path_to_source)
        print(text)
    except Exception:
        traceback.print_exc()



if __name__ == "__main__":
    recorder = SimpleAudioRecorder()

    with SimpleAudioRecorder() as recorder:
        fw = ObjectWatcher("./res/haarcascade_frontalface_default.xml", 0)
        fw.register_object_entered_callback(recorder.start_recording, "output.wav")
        fw.register_object_entered_callback(print, "recording!")

        fw.register_object_left_callback(recorder.stop_recording)
        fw.register_object_left_callback(print, "done recording!")
        fw.register_object_left_callback(transcribe_and_print, "output.wav")

        fw.start()

        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            fw.terminate()
            fw.join()
