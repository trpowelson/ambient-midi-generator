import mido, random
from mido import MidiFile, MidiTrack, Message, MetaMessage
from music_utilities import *


class MusicSection:

    def __init__(self, track):
        """
        Initialize the music section

        Args:
            track (MidiTrack): The instance of MidiTrack to add notes to
        """
        self.track = track
        self.prev_chord_duration = 0
        self.next_time=0
        self.time_added=0
        self.num_chords_added=0

    def update_chord_tracking_info(self, chord_duration):
        """
        Update the tracking information for the next chord to be added.  Each routine that adds
        chords should call this after the chord is added.

        Args:
            chord_duration (int): duration of the chord that was just added
        """
        self.next_time=chord_duration-self.time_added
        self.prev_chord_duration=chord_duration
        self.num_chords_added+=1

    # Routines with logic for each specific chord type.  Each of these
    # routines is responsible for:
    #  - setting self.time_added to track how many notes were added
    #  - calling update_chord_tracking_info so we can track information for the next chord

    def add_empty_chord(self, chord_duration):
        """
        Add an empty chord to the track.  This is used to add a rest between chords.

        Args:
            chord_duration (int): duration of empty chord to add
        """
        # Save information about this chord so we have it when adding the next chord
        self.time_added=0
        self.update_chord_tracking_info(self.next_time+chord_duration)


    def add_regular_chord(self, chord, chord_duration):
        """
        Add a regular chord, where all notes are played at the same time for the entire duration

        Args:
            chord (string): chord to add
            chord_duration (int): duration of chord to add
        """
        octave=4
        for note_num, note_str in enumerate(chord):
            note=note_to_number(note_str, octave)
            if note_num == 0:
                start_time=self.next_time
            else:
                start_time=0
            self.track.append(Message('note_on', note=note, velocity=64, time=start_time))
        for note_num, note_str in enumerate(chord):

            # We want all notes in the chord to be the same length, and have to account
            # for how the note_off gets processed.  The first note should get added
            # with the full time duration.  Any subsequent notes should have the same
            # end time as the first note, so end_time is set to 0
            if note_num == 0:
                end_time=chord_duration
            else:
                end_time=0

            # Convert the note to its numeric value for the given octave
            note=note_to_number(note_str, octave)
            self.track.append(Message('note_off', note=note, velocity=64, time=end_time))

        # Save information about this chord so we have it when adding the next chord
        self.time_added=chord_duration
        self.update_chord_tracking_info(chord_duration)

    def add_melody_chord(self, chord, chord_duration):
        """
        Add a melody chord, where one note of the chord is played at a time for the entire duration

        Args:
            chord (string): chord to add
            chord_duration (int): duration of chord to add
        """
        octave=4
        chord_duration_bars=int(chord_duration/TICKS_PER_BAR)
        mel_note_duration1_bars=0
        mel_note_duration2_bars=0
        mel_note_duration3_bars=0

        for note_num, note_str in enumerate(chord):
            note=note_to_number(note_str, octave)
            if note_num==0:
                # When we get to the first note, first we find the times for this note and the next
                # two notes.
                # The first two notes are random length
                rand_upper_bound=round(chord_duration_bars/2)
                if rand_upper_bound==0:
                    rand_upper_bound=1
                mel_note_duration1_bars=random.randint(1,rand_upper_bound)

                if mel_note_duration1_bars<chord_duration_bars:
                    mel_note_duration2_bars=
                         random.randint(1,(chord_duration_bars-mel_note_duration1_bars))
                    # The last note will be the remainder of the bar (or 0 if the first two notes
                    # add up to 8 bars)
                    mel_note_duration3_bars=
                         (chord_duration_bars-(mel_note_duration1_bars+mel_note_duration2_bars))

                # Add this first note to the melody track
                self.track.append(Message('note_on', note=note, velocity=64, time=self.next_time))
                self.track.append(Message('note_off', note=note, velocity=64,
                                          time=mel_note_duration1_bars*TICKS_PER_BAR))
            if note_num==1 and mel_note_duration2_bars > 0:
                # The second note has time=0 to start immediately after the first
                self.track.append(Message('note_on', note=note, velocity=64, time=0))
                self.track.append(Message('note_off', note=note, velocity=64,
                                          time=mel_note_duration2_bars*TICKS_PER_BAR))
            if note_num==2 and mel_note_duration3_bars > 0:
                # The third note has time=0 to start immediately after the second
                self.track.append(Message('note_on', note=note, velocity=64, time=0))
                self.track.append(Message('note_off', note=note, velocity=64,
                                          time=mel_note_duration3_bars*TICKS_PER_BAR))

        # Save information about this chord so we have it when adding the next chord
        self.time_added=chord_duration
        self.update_chord_tracking_info(chord_duration)

    def add_accent_chord(self, chord, chord_duration, starting_offset, accent_full_modifier=False):
        """
        Add an accent chord, where notes from the chord are played one after the other

        Args:
            chord (string): chord to add
            chord_duration (int): duration of chord to add
            starting_offset (int): offset into the chord to start the accent
            accent_full_modifier (bool): if true, the sequence is played for the entire duration of
                                         the chord.
                                         if false, notes are played for random durations
        """
        octave=4
        if accent_full_modifier == True:
            num_accents= MAX_ACCENTS_IN_SECTION
            accent_time=round(TICKS_PER_BAR/(4)) # 1/2, 1/4, or 1/8 bar
            accent1_offset=0
        else:
            num_accents=random.randint(2,30)
            accent_time=round(TICKS_PER_BAR/(2**random.randint(0,2))) # 1/2, 1/4, or 1/8 bar
            accent1_offset = TICKS_PER_BAR*starting_offset
        octave_offset=0


        # the accent note starts at the offset past the start of the chord
        self.next_time+=accent1_offset

        added_accents_total_time=0
        accent_num=0
        while added_accents_total_time <= chord_duration:
            accent_num+=1
            if accent_num>num_accents:
                break

            if accent_num%3==0:
                octave_offset=random.randint(-2,2)
            note_str=chord[accent_num%3]
            note=note_to_number(note_str, octave+octave_offset)


            if accent_num==1:
                self.track.append(Message('note_on', note=note, velocity=64, time=self.next_time))
                self.track.append(Message('note_off', note=note, velocity=64, time=accent_time))

                # Reset the time since we started a new chord
                added_accents_total_time=accent1_offset+accent_time
            else:
                if added_accents_total_time+accent_time < chord_duration:
                    self.track.append(Message('note_on', note=note, velocity=64, time=0))
                    self.track.append(Message('note_off', note=note, velocity=64, time=accent_time))
                    added_accents_total_time+=accent_time

        # Save information about this chord so we have it when adding the next chord
        self.time_added=added_accents_total_time
        self.update_chord_tracking_info(chord_duration)
