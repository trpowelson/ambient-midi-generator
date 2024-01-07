# Ambient MIDI Generator
Python scripts to generate MIDI for ambient music

## Usage
Update `__main__.py` to set the parameters (tempo, song key, etc), then run:
`python -m  ambient_midi_generator`

This generates a file named `midi-output.mid`, which can then be imported into a DAW such as Ableton, Pro Tools, REAPER, etc.

## Requirements
Python 3.10 or above

Dependencies include [MIDO](https://pypi.org/project/mido/) and [MINGUS](https://bspaans.github.io/python-mingus/)

To install the dependencies, use: `pip install mido, mingus`

## FAQ
### What is MIDI?
MIDI is the Musical Instrument Digital Interface, which is used to represent musical notes

### What do I do with the output MIDI file that is generated?
This should be imported into a DAW (Digital Audio Workstation), and each track should be assigned a different instrument

### What instruments work best?
For the first track which has straight chords, an ambient/droning type instrument works well.  I have been using [Hybernate](https://rigid-audio.com/products_hibernate.html) from Rigid Audio.  For a free option, consider looking at [Spitfire LABS](https://labs.spitfireaudio.com/?sortBy=prod_products_labs_popular) or [Vital](https://vital.audio/).

For all the other tracks, experiment with different sounds.  I tend to like a mix of instrument types, some with subtle sounds and some that are more pronounced.

### What is the music used for?
This makes ambient music which could be helpful for studying or background music.  Feel free to experiment with different parameters to try different music types.
