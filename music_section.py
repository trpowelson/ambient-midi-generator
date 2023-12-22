import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}


def swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'

    return note


def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']
    return note


class music_section:
    
    
    def __init__(self, track, chord_duration):
        self.track = track
        self.chord_duration = chord_duration
        #self.time_delta=0
        self.next_time=0
        
    def add_chord(self, chord):
        print("adding chord: ", str(chord))
        note_num=0
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, 4)
            self.track.append(Message('note_on', note=note, velocity=64, time=0))
        note_num=0
        time_delta=0
        for note_str in chord:
            note_num=note_num+1
            note=note_to_number(note_str, 4)
            self.track.append(Message('note_off', note=note, velocity=64, time=self.chord_duration-time_delta))
          #  self.time_delta=self.chord_duration
            time_delta=self.chord_duration
        self.next_time=self.next_time+self.chord_duration
    