"""
Module containing helper functions and global variables
"""

# List of all possible notes
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

# List of all possible octaves
OCTAVES = list(range(11))

NOTES_IN_OCTAVE = len(NOTES)

MAX_ACCENTS_IN_SECTION = 1000

TICKS_PER_BAR = 1920

note_errors = {
    'bad_note': 'Input note was not C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, or B',
    'bad_octave': 'Input octave was not 0-10',
    'bad_note_number': 'Note out of range 0-127'
}

def swap_accidentals(note):
    """
    Swaps accidentals to their enharmonic equivalent
    Args:
        note (string): input note

    Returns:
        note (string): output note, with accidentals swapped
    """
    ret_note= note
    match note:
        case 'Db':
            ret_note= 'C#'
        case 'D#':
            ret_note= 'Eb'
        case 'E#':
            ret_note= 'F'
        case 'Gb':
            ret_note= 'F#'
        case 'G#':
            ret_note= 'Ab'
        case 'A#':
            ret_note= 'Bb'
        case 'B#':
            ret_note= 'C'

    return ret_note

def note_to_number(note: str, octave: int) -> int:
    """
    Converts a note and octave to a MIDI note number

    Args:
        note (str): input note
        octave (int): octave desired for input note

    Returns:
        int: output MIDI note number
    """
    note = swap_accidentals(note)
    assert note in NOTES, note_errors['bad_note']
    assert octave in OCTAVES, note_errors['bad_octave']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, note_errors['bad_note_number']
    return note
