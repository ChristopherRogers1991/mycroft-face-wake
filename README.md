# mycroft-face-wake
Trigger Mycroft without the use of a wake word.

Currently this can detect a person's face, and record audio. Recording begins when the person looks at the camera,
and ends when they look away. Soon it will transcribe that audio, and send the text to Mycroft.

To test the existing functionality, clone the repo, run `pip install -r requirements.txt && pip install .` from the project root,
and run `python3 main.py` (it'll keep running/overwriting the same file until you ctrl+c it).
