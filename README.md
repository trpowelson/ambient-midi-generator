# Ambient MIDI Generator
Python scripts to generate MIDI for ambient music

## Usage
Update main.py to set the parameters (tempo, song key, etc), then run:
`python main.py`

This generates a file named `midi-output.mid`, which can then be imported into a DAW such as Ableton, Pro Tools, REAPER, etc.

## Requirements
This is tested using Python 3.12.1, and should work with any version of Python 3.

Dependencies include [MIDO](https://pypi.org/project/mido/) and [MINGUS](https://bspaans.github.io/python-mingus/)

To install the dependencies, use: `pip install mido, mingus`

## FAQ
### What is MIDI?
MIDI is the Musical Instrument Digital Interface, which is used to represent musical notes

### What do I do with the output MIDI file that is generated?
This should be imported into a DAW (Digital Audio Workstation), and each track should be assigned a different instrument

### What instruments work best?
For the first track which has straight chords, an ambient/droning type instrument works well.  I have been using [Hybernate](https://rigid-audio.com/products_hibernate.html) from Rigid Audio For a free option, consider looking at [Vital](https://vital.audio/) and experimenting with different presets such as Salomon.

For all the other tracks, experiment with different sounds.  I tend to like a mix of instrument types, some with subtle sounds and some that are more pronounced.

### What is the music used for?
This makes ambient music which could be helpful for studying or background music.  Feel free to experiment with different parameters to try different music types.
