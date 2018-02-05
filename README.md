# mycroft-face-wake

Trigger Mycroft without the use of a wake-word.

## Simple Demonstration
Short demo: https://www.youtube.com/watch?v=H9P5TRo8nQs&feature=youtu.be

Longer explanation and demo: https://www.youtube.com/watch?v=ytKUTBfjnQI

## Description and Motivation

This is a working prototype. It offers no configuration, must be run on the same host
as [mycroft-core](https://github.com/MycroftAI/mycroft-core), and all STT is handled
by Google's API (via the [SpeechRecognition library](https://pypi.python.org/pypi/SpeechRecognition/)).
It does not replace the wake-word functionality - they can both used at the same time.

I feel that this may offer a more natural way to interact with a voice assistant. Wake words are great,
but often when I talk to people, I just make eye-contact and begin talking. This emulates that type of
interaction (though again, it does not replace the wake-word functionality).

This runs quite nicely on my desktop and laptop, but a Raspberry Pi is not quite powerful enough to handle
it effectively (in my brief test, it took roughly 4 seconds to detect a face on the Pi, where it happens
virtually instantanesouly on a desktop/laptop). Note that there is also some extra work to get this running
on a Pi - it will not work as-is. I may add support at a later date, however, given the performance, it
is not a priority.

## Usage

1) `git clone https://github.com/ChristopherRogers1991/mycroft-face-wake.git`
2) `cd mycroft-face-wake && pip install -r requirements.txt && pip install .`
3) `python main.py`
