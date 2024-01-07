"""
main.py

Module that creates a random, generative MIDI file.

"""
import random
import mido
from mido import MidiFile, MidiTrack, MetaMessage
from mingus.core import chords, scales, progressions

from ambient_midi_generator.common.music_utilities import TICKS_PER_BAR
from ambient_midi_generator.common.music_section import MusicSection



song_scale_notes=[]
TEMPO=0
song_part_info = []

def generate_chord_sequence(num_chords,song_key,first_chord_sequence):
    """
    Generates the chord sequence we will use for this section of the song.
    All chords will be in the song's key.

    Args:
        num_chords (int): how many chords to generate
        song_key (str): key of section, e.g. 'C'
        first_chord_sequence (array of strings): first chords to use for this section of the song.
                                                 Use random chords in key after this sequence.

    Returns:
        chord_sequence (list): List of chords to use for this section of the song,
                               e.g. ["Cmaj7", "Dmin7", "Gmaj7" , ...]
    """
    global song_scale_notes
    song_scale_notes = scales.get_notes(song_key)

    # Create list of possible chords to use in this section
    chord_list_shorthand = []
    for suffix in ["maj", "min", "maj7","min7"]:
        for note in song_scale_notes:
            chord_list_shorthand.append(note+suffix)

    # Create a list to store the generated chord sequence
    chord_sequence = []

    # If the user passed in a first chord sequence, add it to the chord sequence
    if len(first_chord_sequence) > 0:
        chord_sequence += progressions.to_chords(first_chord_sequence, song_key)
        # Subtract the number of chords we just added from the total number of chords
        num_chords -= len(first_chord_sequence)

    assert len(chord_sequence) <= num_chords, "Num chords not long enough for first chord sequence"
    print("Generating MIDI tracks with chord sequence: " + str(chord_sequence))

    # Generate random chord sequence
    for _ in range(num_chords):
        chord_in_key=False
        while not chord_in_key:
            chord_to_add = random.choice(chord_list_shorthand)
            chord_in_key = test_chord_in_key(chord_to_add)

        chord_sequence.append(chords.from_shorthand(chord_to_add))

    return chord_sequence

def test_chord_in_key(chord) -> bool:
    """
    Tests if the input chord is within the current key.

    Args:
        chord (string): Shorthand of the chord to test, e.g. 'Cmaj7'
    Output:
        bool: True if the chord is in the current key, False otherwise
    """
    chord_notes=chords.from_shorthand(chord)
    ret_val=True
    for note in chord_notes:
        if note not in song_scale_notes:
            ret_val=False
    return ret_val

def create_midi_file(output_file):
    """
    Creates a MIDI file with a random chord progression, and populates
    it with multiple tracks.

    Args:
        output_file (string): name of the MIDI file to create
    """

    mid = MidiFile(type=1)

    # Create each track
    chord_track = MidiTrack()
    melody_track = MidiTrack()
    accent_track = MidiTrack()
    accent_track_2 = MidiTrack()
    full_accent_track = MidiTrack()
    key_change_track = MidiTrack()

    # Set the name of each track
    chord_track.append(MetaMessage('track_name', name='Chord track'))
    melody_track.append(MetaMessage('track_name', name='Melody track'))
    accent_track.append(MetaMessage('track_name', name='Accent track'))
    accent_track_2.append(MetaMessage('track_name', name='Accent track 2'))
    full_accent_track.append(MetaMessage('track_name', name='Full accent track'))
    key_change_track.append(MetaMessage('track_name', name='Key change track'))

    # Add each track to the MIDI file
    mid.tracks.append(chord_track)
    mid.tracks.append(melody_track)
    mid.tracks.append(accent_track)
    mid.tracks.append(accent_track_2)
    mid.tracks.append(full_accent_track)
    mid.tracks.append(key_change_track)

    # Set microseconds per beat based on the input tempo
    us_per_beat=int(mido.tempo2bpm(TEMPO))
    chord_track.append(MetaMessage('set_tempo', tempo=us_per_beat))

    # Initialize music sections for each of our tracks
    chord_section=MusicSection(chord_track)
    melody_section=MusicSection(melody_track)
    accent_section=MusicSection(accent_track)
    accent_section_2=MusicSection(accent_track_2)
    full_accent_section=MusicSection(full_accent_track)
    key_change_section=MusicSection(key_change_track)

    # The first loop is for each section of the song, which has its own key
    for part_num, song_part in enumerate(song_part_info):
        chord_duration_bars_choices = song_part["Chord duration bar choices: "]
        num_chords = song_part["num_chords: "]
        song_key = song_part["Key: "]
        accent1_offset_bars = song_part["Accent 1 offset bars: "]
        first_chord_sequence = song_part["first chord sequence"]
        chord_sequence = generate_chord_sequence(num_chords,song_key,first_chord_sequence)

        print("Creating section with " + str(num_chords) + " chords, key of " + song_key +
              ", and accent 1 offset of " + str(accent1_offset_bars) + " bars.")


        # Add each chord to each track
        for chord_num, chord in enumerate(chord_sequence):
            chord_duration_bars=random.choice(chord_duration_bars_choices)
            chord_duration = chord_duration_bars*TICKS_PER_BAR

            while True:
                if random.randint(0,9) == 0:
                    chord_section.add_empty_chord(chord_duration)
                else:
                    chord_section.add_regular_chord(chord,chord_duration)

                melody_section.add_melody_chord(chord,chord_duration)

                if random.randint(0,1) == 1:
                    accent_section.add_accent_chord(chord,chord_duration,1)
                else:
                    accent_section.add_empty_chord(chord_duration)

                if random.randint(0,1) == 1:
                    accent_section_2.add_accent_chord(chord,chord_duration,2)
                else:
                    accent_section_2.add_empty_chord(chord_duration)

                full_accent_section.add_accent_chord(chord,chord_duration,0,True)

                if part_num != 0 and chord_num==0:
                    key_change_section.add_regular_chord(chord,chord_duration)
                else:
                    key_change_section.add_empty_chord(chord_duration)

                # If the chord length is 1 bar, we will randomly repeat the same chord
                if chord_duration_bars == 1:
                    if random.randint(0,1) == 1:
                        break
                else:
                    break


    # Save the MIDI file
    mid.save(output_file)
    print(f"MIDI file '{output_file}' generated successfully.")

if __name__ == "__main__":

    TEMPO = 60 # Tempo in BPM

    song_part_info = [{"Chord duration bar choices: ": [1,2,4,8,16],
                      "num_chords: ": 8,
                      "first chord sequence": ["I","V","vi","IV"],
                      "Key: ": "A",
                      "Accent 1 offset bars: ": 1},

                      {"Chord duration bar choices: ": [2,4,8],
                      "num_chords: ": 4,
                      "first chord sequence": [],
                      "Key: ": "f",
                      "Accent 1 offset bars: ": 1},

                      {"Chord duration bar choices: ": [1,2,4],
                      "num_chords: ": 4,
                      "first chord sequence": [],
                      "Key: ": "C",
                      "Accent 1 offset bars: ": 2},
                      ]


    FILENAME="midi-output.mid"
    create_midi_file(FILENAME)
