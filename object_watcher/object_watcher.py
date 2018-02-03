import cv2
import time
from threading import Thread
import dlib

class ObjectWatcher(Thread):

    def __init__(self,
                 haarcascade_path="haarcascade_frontalface_default.xml",
                 device=0):
        super().__init__(name="object_watcher")
        self._cascade = cv2.CascadeClassifier(haarcascade_path)
        self._detector = dlib.get_frontal_face_detector()
        self._video_capture = cv2.VideoCapture(device)
        self._call_backs = {"object_entered" : [], "object_left" : []}
        self._terminate = False

    def terminate(self):
        self._terminate = True

    def register_object_entered_callback(self, callable, *args, **kwargs):
        self._call_backs["object_entered"].append((callable, args, kwargs))

    def register_object_left_callback(self, callable, *args, **kwargs):
        self._call_backs["object_left"].append((callable, args, kwargs))

    def device_is_ready(self, timeout=5):
        if timeout == 0:
            while not self._video_capture.isOpened():
                time.sleep(1)
        elif timeout > 0:
            start = time.time()
            while start - time.time() < timeout and not \
                    self._video_capture.isOpened():
                time.sleep(1)
        return self._video_capture.isOpened()

    def object_present(self):
        ret, frame = self._video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # objects = self._cascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.1,
        #     minNeighbors=5,
        #     minSize=(30, 30)
        # )
        objects = self._detector(gray, 0)
        return len(objects) > 0

    def _run_callbacks(self, callbacks):
        for callable, args, kwargs in self._call_backs[callbacks]:
            callable(*args, **kwargs)

    def run(self):
        while not self._terminate:
            if self.object_present():
                self._run_callbacks("object_entered")
                while self.object_present() and not self._terminate:
                    pass
                else:
                    self._run_callbacks("object_left")
        else:
            self._video_capture.release()
            self._terminate = False

if __name__ == '__main__':
    fw = ObjectWatcher("../res/haarcascade_frontalface_default.xml", 0)
    fw.register_object_entered_callback(print, "face entered!")
    fw.register_object_left_callback(print, "face left!")
    fw.register_object_left_callback(print)
    fw.start()
    time.sleep(10)
    fw.terminate()
    fw.join()
