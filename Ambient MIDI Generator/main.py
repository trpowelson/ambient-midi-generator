# With help from:
#https://medium.com/@stevehiehn/how-to-generate-music-with-python-the-basics-62e8ea9b99a5


import mido, random
from mido import MidiFile, MidiTrack, Message, MetaMessage
from mingus.core import chords, scales, progressions

from music_utilities import *
from music_section import *



def generate_chord_sequence(num_chords=4):
    chord_list_shorthand = []
    for n in NOTES:
        chord_list_shorthand.append(n+"maj7")
        chord_list_shorthand.append(n+"min7")
    
    #print(chords.from_shorthand("Cmaj7"))

    # Create a list to store the generated chord sequence
    chord_sequence = []
    chord_sequence += progressions.to_chords(["I","V","vi","IV"], song_key)
    print("Generating MIDI tracks with chord sequence: " + str(chord_sequence))

    # Generate random chord sequence
    for _ in range(num_chords):
        chord_in_key=False
        while not chord_in_key:
            chord_to_add = random.choice(chord_list_shorthand)
            chord_in_key = test_chord_in_key(chord_to_add)

        chord_sequence.append(chords.from_shorthand(chord_to_add))

    return chord_sequence

def test_chord_in_key(chord):
    chord_notes=chords.from_shorthand(chord)
    for note in chord_notes:
        if note not in song_scale_notes:
            return False
    return True

def create_midi_file(chord_sequence, output_file):
    
    mid = MidiFile(type=1)
    TICKS_PER_BAR = mid.ticks_per_beat*4
    
    chord_track = MidiTrack()
    melody_track = MidiTrack()
    accent_track = MidiTrack()
    full_accent_track = MidiTrack()
    mid.tracks.append(chord_track)
    mid.tracks.append(melody_track)
    mid.tracks.append(accent_track)
    mid.tracks.append(full_accent_track)

    # Set tempo, in microseconds per beat
    us_per_beat=int(mido.tempo2bpm(tempo))
    chord_track.append(MetaMessage('set_tempo', tempo=us_per_beat))

    # Initialize music sections for each of our tracks
    chord_section=music_section(chord_track)
    melody_section=music_section(melody_track)
    accent_section=music_section(accent_track)
    full_accent_section=music_section(full_accent_track)


    # Add each chord to each track
    for chord in chord_sequence:
        chord_duration_bars=random.choice(chord_duration_bars_choices)
        chord_duration = chord_duration_bars*TICKS_PER_BAR
        
        while True:
            chord_section.add_regular_chord(chord,chord_duration)
            melody_section.add_melody_chord(chord,chord_duration)
            if random.randint(0,1) == 1:
                accent_section.add_accent_chord(chord,chord_duration)
            else:
                accent_section.add_empty_chord(chord_duration)

            full_accent_section.add_accent_chord(chord,chord_duration,True)
            
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
    num_chords = 20  # Change this value to generate a different number of chords
    tempo = 60 # Tempo in BPM
    chord_duration_bars_choices = [1,2,4,8,16]
    song_key = "G"  # uppercase for major, lowercase for minor
    song_scale_notes = scales.get_notes(song_key)
    accent1_offset_bars = 1
    
    print(str(song_scale_notes))
    chord_sequence = generate_chord_sequence(num_chords)
    filename="midi-output.mid"
    create_midi_file(chord_sequence,filename)
