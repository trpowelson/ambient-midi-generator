import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
from music_utilities import *


class music_section:
    
    
    def __init__(self, track):
        self.track = track
        self.prev_chord_duration = 0
        self.next_time=0
        self.time_added=0
        self.num_chords_added=0
        
        
    def add_chord(self, chord, chord_duration, chord_type):
        print("adding chord: ", str(chord))
        if chord_type == ChordType.REGULAR:
            self.add_regular_chord(chord, chord_duration)
            
        self.next_time=chord_duration-self.time_added
        self.prev_chord_duration=chord_duration
        self.num_chords_added+=1
    
    def add_regular_chord(self, chord, chord_duration):
        octave=4
        note_num=0
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, octave)
            self.track.append(Message('note_on', note=note, velocity=64, time=self.next_time))
        note_num=0
        for note_str in chord:
            note_num=note_num+1
            
            # We want all notes in the chord to be the same length, and have to account
            # for how the note_off gets processed.  The first note should get added
            # with the full time duration.  Any subsequent notes should have the same
            # end time as the first note, so end_time is set to 0            
            if note_num== 1:
                end_time=chord_duration
            else:
                end_time=0
                
            # Convert the note to its numeric value for the given octave
            note=note_to_number(note_str, octave)
            self.track.append(Message('note_off', note=note, velocity=64, time=end_time))
        
        # Save information about this chord so we have it when adding the next chord
        self.time_added=chord_duration

