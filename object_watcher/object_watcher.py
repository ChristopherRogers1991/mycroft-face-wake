import cv2
import time
from threading import Thread

class ObjectWatcher(Thread):

    def __init__(self, device=0, delay=.2, detector=None):
        """

        Parameters
        ----------
        device : int
            The video device index, passed directly to cv2.VideoCapture
        delay : float
            To reduce false poitives/noise, the object must be present
            for at lease this many seconds before it will be registered.
        detector : callable
            This must take a single frame as it's only argument, and
            return a true or false value indicating whether the object
            is present. See `create_haar_cascade_detector` and
            `create_dlib_frontal_face_detector` for examples.
        """
        super().__init__(name="object_watcher")
        self._video_capture = cv2.VideoCapture(device)
        self._delay = delay
        self._detector = detector

        self._call_backs = {"object_entered" : [], "object_left" : []}
        self._terminate = False
        self._time_of_first_face = None

    def terminate(self):
        """
        Terminate the object detection thread.

        """
        self._terminate = True

    def register_object_entered_callback(self, callable, *args, **kwargs):
        """
        Callbacks are called in the order in which they were registered.

        Parameters
        ----------
        callable : callable
            This will be called when the object is detected within the frame.
        args : list
            Passed to callable.
        kwargs : dict
            Passed to callable

        """
        self._call_backs["object_entered"].append((callable, args, kwargs))

    def register_object_left_callback(self, callable, *args, **kwargs):
        """
        Callbacks are called in the order in which they were registered.

        Parameters
        ----------
        callable : callable
            This will be called when the object leaves the frame.
        args : list
            Passed to callable.
        kwargs : dict
            Passed to callable

        """
        self._call_backs["object_left"].append((callable, args, kwargs))

    def device_is_ready(self, timeout=5):
        """
        Currently unused. Likely to be removed.

        Parameters
        ----------
        timeout : int

        Returns
        -------
        boolean

        """
        if timeout == 0:
            while not self._video_capture.isOpened():
                time.sleep(1)
        elif timeout > 0:
            start = time.time()
            while start - time.time() < timeout and not \
                    self._video_capture.isOpened():
                time.sleep(1)
        return self._video_capture.isOpened()

    def _object_present(self):
        """

        Returns
        -------
        boolean
            True if the object has been within frame for at
            self._delay seconds.

        """
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
        """
        Overridden from Thread.

        Do not call this directly! Call `.start()` to
        start the thread.

        """
        while not self._terminate:
            if self._object_present():
                self._run_callbacks("object_entered")
                while self._object_present() and not self._terminate:
                    pass
                else:
                    self._run_callbacks("object_left")
        else:
            self._video_capture.release()
            self._terminate = False


def create_haar_cascade_detector(path_to_haarcascade):
    """

    Parameters
    ----------
    path_to_haarcascade : str
        The path to a haarcascade XML file.

    Returns
    -------
    function
        A function that can be used as a detector. In an
        ObjectWatcher. It takes in a single frame, and
        returns a boolean, True if the object represented
        by the given haarcascade is within the frame.

    """
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
    """

    Returns
    -------
    function
        A function that can be used as a detector in an
        ObjectWatcher. Returns true if a face is detected
        within the frame.

    """
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
