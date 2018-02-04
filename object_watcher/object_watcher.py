import cv2
import time
from threading import Thread

class ObjectWatcher(Thread):

    def __init__(self, device=0, delay=.2, detector=None):
        super().__init__(name="object_watcher")
        self._video_capture = cv2.VideoCapture(device)
        self._delay = delay
        self._detector = detector

        self._call_backs = {"object_entered" : [], "object_left" : []}
        self._terminate = False
        self._time_of_first_face = None

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

        face_found = self._detector(frame)

        if not face_found:
            self._time_of_first_face = None
            return False

        now = time.time()

        if not self._time_of_first_face:
            self._time_of_first_face = now
            return False
        if now - self._time_of_first_face > self._delay:
            return True
        return False

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


def create_haar_cascade_detector(path_to_haarcascade):
    cascade = cv2.CascadeClassifier(path_to_haarcascade)
    def detector(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        return len(objects) > 0
    return detector


def create_dlib_frontal_face_detector():
    import dlib
    frontal_face_detector = dlib.get_frontal_face_detector()
    def detector(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frontal_face_detector(gray, 0)
    return detector



if __name__ == '__main__':
    fw = ObjectWatcher(detector=create_dlib_frontal_face_detector())
    fw.register_object_entered_callback(print, "face entered!")
    fw.register_object_left_callback(print, "face left!")
    fw.register_object_left_callback(print)
    fw.start()
    time.sleep(10)
    fw.terminate()
    fw.join()
