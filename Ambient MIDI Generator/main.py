# With help from:
#https://medium.com/@stevehiehn/how-to-generate-music-with-python-the-basics-62e8ea9b99a5


import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import random
from mingus.core import chords, scales, progressions

from music_utilities import *
from music_section import *



def generate_chord_sequence(num_chords=4):
    chord_list_shorthand = [
    ]
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

def create_midi_file(chord_sequence, output_file="output.mid", OCTAVE=4):   
    

    mid = MidiFile(type=1)
    TICKS_PER_BAR = mid.ticks_per_beat*4
    
    track = MidiTrack()
    melody_track = MidiTrack()
    accent_track = MidiTrack()
    test_track = MidiTrack()
    mid.tracks.append(track)
    mid.tracks.append(melody_track)
    mid.tracks.append(accent_track)
    mid.tracks.append(test_track)

    # Set tempo, in microseconds per beat
    us_per_beat=int(mido.tempo2bpm(tempo))
    track.append(MetaMessage('set_tempo', tempo=us_per_beat))

    # Add chords to the MIDI track
    chord_num=0
    added_accents_total_time=0

    my_test_section=music_section(test_track)

    for chord in chord_sequence:
        chord_duration_bars=random.choice(chord_duration_bars_choices)
        print(f"Chord {chord_num} duration: {chord_duration_bars} bars")
        chord_duration = TICKS_PER_BAR*chord_duration_bars  # Duration of each chord in ticks (adjust as needed)
        accent1_offset = TICKS_PER_BAR*accent1_offset_bars
        
        my_test_section.add_chord(chord,TICKS_PER_BAR*chord_duration_bars,ChordType.REGULAR)
        
        chord_num=chord_num+1
        time_delta=0
        note_num=0
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, OCTAVE)
            track.append(Message('note_on', note=note, velocity=64, time=0))
            
            if note_num==1:
                # When we get to the first note, first we find the times for this note and the next two notes
                # The first two notes are random length
                mel_note_duration1_bars=random.randint(1,round(chord_duration_bars/2))
                mel_note_duration2_bars=random.randint(1,(chord_duration_bars-mel_note_duration1_bars))
                # The last note will be the remainder of the bar (or 0 if the first two notes add up to 8 bars)
                mel_note_duration3_bars=(chord_duration_bars-(mel_note_duration1_bars+mel_note_duration2_bars))
                
                # Add this first note to the melody track
                melody_track.append(Message('note_on', note=note, velocity=64, time=0))
                melody_track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration1_bars*TICKS_PER_BAR))
            if note_num==2:
                # The second note has time=0 to start immediately after the first
                melody_track.append(Message('note_on', note=note, velocity=64, time=0))
                melody_track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration2_bars*TICKS_PER_BAR))
            if note_num==3 and mel_note_duration3_bars > 0:
                # The third note has time=0 to start immediately after the second
                melody_track.append(Message('note_on', note=note, velocity=64, time=0))
                melody_track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration3_bars*TICKS_PER_BAR))
        
        num_accents=random.randint(2,30)
        accent_time=round(TICKS_PER_BAR/(2**random.randint(0,2))) # 1/2, 1/4, or 1/8 note
        octave_offset=0
        for accent_num in range(1,num_accents):
            if accent_num%3==0:
                octave_offset=random.randint(-2,2)
            note_str=chord[accent_num%3]
            note=note_to_number(note_str, OCTAVE+octave_offset)
            
                        
            if accent_num==1:
                if chord_num==1:
                    accent_track.append(Message('note_on', note=note, velocity=64, time=accent1_offset))
                    accent_track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                    added_accents_total_time+=accent_time+accent1_offset
                else:
                    if accent1_offset+prev_chord_duration-added_accents_total_time>=0:
                        # This is the first accent on a chord other than the first one.  
                        # Add the accent note to the start of where the next chord starts, plus the start offset within the chord
                        print("added" + str(added_accents_total_time))
                        print("chord_duration" + str(chord_duration))
                        accent_track.append(Message('note_on', note=note, velocity=64, time=accent1_offset+prev_chord_duration-added_accents_total_time))
                        accent_track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                
                added_accents_total_time=accent1_offset+accent_time # Reset the time since we started a new chord
            
                prev_chord_duration=chord_duration #remember this chord's length so we can use it to get the start time of the next chord
            else:
                if added_accents_total_time+accent_time < chord_duration:
                    accent_track.append(Message('note_on', note=note, velocity=64, time=0))
                    accent_track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                    added_accents_total_time+=accent_time

        note_num=0
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, OCTAVE)
            track.append(Message('note_off', note=note, velocity=64, time=chord_duration-time_delta))
            time_delta=chord_duration
            

    # Save the MIDI file
    mid.save(output_file)
    print(f"MIDI file '{output_file}' generated successfully.")

if __name__ == "__main__":
    num_chords = 4  # Change this value to generate a different number of chords
    tempo = 60 # Tempo in BPM
    chord_duration_bars_choices = [2,4,8,16]
    print("test constant "+str(test_constant))
    song_key = "f"  # uppercase for major, lowercase for minor
    song_scale_notes = scales.get_notes(song_key)
    accent1_offset_bars = 1
    
    print(str(song_scale_notes))
    chord_sequence = generate_chord_sequence(num_chords)
    create_midi_file(chord_sequence)
