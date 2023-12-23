import mido, random
from mido import MidiFile, MidiTrack, Message, MetaMessage
from music_utilities import *



class music_section:
    
    
    def __init__(self, track):
        self.track = track
        self.prev_chord_duration = 0
        self.next_time=0
        self.time_added=0
        self.num_chords_added=0
        
    # General routine for adding chords, this will call helper routines that have more
    # specific chord logic
    def add_chord(self, chord, chord_duration, chord_type):
        print("adding chord: ", str(chord))
        match chord_type:
            case ChordType.REGULAR:
                self.add_regular_chord(chord, chord_duration)
            case ChordType.MELODY:
                self.add_melody_chord(chord, chord_duration)
            case ChordType.ACCENT:
                self.add_accent_chord(chord, chord_duration)
                    
        self.next_time=chord_duration-self.time_added
        self.prev_chord_duration=chord_duration
        self.num_chords_added+=1
    
    # Helper routines with logic for each specific chord type.  Each of these
    # routines is responsible for setting self.time_added to track how many
    # notes were added, so that the next invocation of add_chord can set
    # the appropriate start times
    
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

    def add_melody_chord(self, chord, chord_duration):
        octave=4
        note_num=0
        chord_duration_bars=int(chord_duration/TICKS_PER_BAR)
        print("chord bars" + str(chord_duration_bars))
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, octave)
            if note_num==1:
                # When we get to the first note, first we find the times for this note and the next two notes
                # The first two notes are random length
                mel_note_duration1_bars=random.randint(1,round(chord_duration_bars/2))
                mel_note_duration2_bars=random.randint(1,(chord_duration_bars-mel_note_duration1_bars))
                # The last note will be the remainder of the bar (or 0 if the first two notes add up to 8 bars)
                mel_note_duration3_bars=(chord_duration_bars-(mel_note_duration1_bars+mel_note_duration2_bars))
                
                # Add this first note to the melody track
                self.track.append(Message('note_on', note=note, velocity=64, time=self.next_time))
                self.track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration1_bars*TICKS_PER_BAR))
            if note_num==2:
                # The second note has time=0 to start immediately after the first
                self.track.append(Message('note_on', note=note, velocity=64, time=0))
                self.track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration2_bars*TICKS_PER_BAR))
            if note_num==3 and mel_note_duration3_bars > 0:
                # The third note has time=0 to start immediately after the second
                self.track.append(Message('note_on', note=note, velocity=64, time=0))
                self.track.append(Message('note_off', note=note, velocity=64, time=mel_note_duration3_bars*TICKS_PER_BAR))
        
        # Save information about this chord so we have it when adding the next chord
        self.time_added=chord_duration

    def add_accent_chord(self, chord, chord_duration):
        octave=4
        note_num=0
        chord_duration_bars=int(chord_duration/TICKS_PER_BAR)
        num_accents=random.randint(2,30)
        accent_time=round(TICKS_PER_BAR/(2**random.randint(0,2))) # 1/2, 1/4, or 1/8 note
        octave_offset=0
        accent1_offset = TICKS_PER_BAR*1
        
        # the accent note starts at the offset past the start of the chord
        self.next_time+=accent1_offset
        
        for accent_num in range(1,num_accents):
            if accent_num%3==0:
                octave_offset=random.randint(-2,2)
            note_str=chord[accent_num%3]
            note=note_to_number(note_str, octave+octave_offset)
            
                        
            if accent_num==1:
                self.track.append(Message('note_on', note=note, velocity=64, time=self.next_time))
                self.track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                
                added_accents_total_time=accent1_offset+accent_time # Reset the time since we started a new chord            
            else:
                if added_accents_total_time+accent_time < chord_duration:
                    self.track.append(Message('note_on', note=note, velocity=64, time=0))
                    self.track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                    added_accents_total_time+=accent_time
        
        # Save information about this chord so we have it when adding the next chord
        self.time_added=added_accents_total_time
