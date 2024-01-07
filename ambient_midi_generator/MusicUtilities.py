"""
utilities.py

Module containing helper functions and global variables
"""

# List of all possible notes
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

# List of all possible octaves
OCTAVES = list(range(11))

NOTES_IN_OCTAVE = len(NOTES)
TICKS_PER_BAR = 1920    # Note once we create the MIDI object we can calculate
                        # and override this value
MAX_ACCENTS_IN_SECTION = 1000

note_errors = {
    'bad_note': 'Input note was not C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, or B',
    'bad_octave': 'Input octave was not 0-10',
    'bad_note_number': 'Note out of range 0-127'
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
    assert note in NOTES, note_errors['bad_note']
    assert octave in OCTAVES, note_errors['bad_octave']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, note_errors['bad_note_number']
    return note