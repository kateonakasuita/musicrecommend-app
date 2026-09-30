import pretty_midi
import random


def transform_midi(input_midi_path, style):

    midi = pretty_midi.PrettyMIDI(input_midi_path)

    if style == "piano":
        program_number = 0
    elif style == "musicbox":
        program_number = 10
    elif style == "jazz":
        program_number = 65
    else:
        program_number = 0

    for instrument in midi.instruments:

        if instrument.is_drum:
            continue

        instrument.program = program_number

        if style == "musicbox":

            for note in instrument.notes:
                note.velocity = min(80, note.velocity)

                delay = (note.pitch % 5) * 0.02
                note.start += delay
                note.end += delay

        elif style == "jazz":

            for note in instrument.notes:
                note.velocity = min(127, int(note.velocity * 1.1))

                random_shift = random.uniform(-0.01, 0.01)
                note.start = max(0, note.start + random_shift)

    return midi


if __name__ == "__main__":

    input_path = "test.mid"

    converted_midi = transform_midi(
        input_path,
        style="musicbox"
    )

    converted_midi.write("test_output.mid")

    print("変換が完了しました。")