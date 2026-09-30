import pretty_midi
import random


def transform_midi(input_midi_path, style):

    # MIDIファイルを読み込む
    midi = pretty_midi.PrettyMIDI(input_midi_path)

    # ==============================
    # 楽器の設定
    # ==============================
    #
    # General MIDIのProgram Number
    #
    # 0  : ピアノ
    # 10 : Music Box（オルゴール）
    # 40 : Violin（バイオリン）
    # 65 : Alto Sax（アルトサックス）
    # 73 : Flute（フルート）
    #
    # 数字を変更すると使用する楽器が変わる。
    # ==============================

    if style == "piano":
        program_number = 0

    elif style == "musicbox":
        program_number = 10

    elif style == "jazz":
        program_number = 65

    else:
        program_number = 0


    # MIDI内の楽器を1つずつ処理する
    for instrument in midi.instruments:

        # ドラムは処理しない
        if instrument.is_drum:
            continue

        # 楽器を変更
        instrument.program = program_number


        # ==============================
        # オルゴール風
        # ==============================

        if style == "musicbox":

            for note in instrument.notes:

                # 音の強さを変更
                #
                # 80を小さくすると、より弱く優しい音になる。
                # 80を大きくすると、より強い音になる。
                note.velocity = min(80, note.velocity)

                # 音の開始時間を少しずらす
                #
                # 0.02を小さくするとズレが小さくなる。
                # 大きくすると音が順番に鳴る感じが強くなる。
                # 大きくしすぎるとリズムが崩れる場合がある。
                delay = (note.pitch % 5) * 0.02

                note.start += delay
                note.end += delay


        # ==============================
        # ジャズ風
        # ==============================

        elif style == "jazz":

            for note in instrument.notes:

                # 音の強さを少し大きくする
                #
                # 1.0 → 変化なし
                # 1.1 → 10%大きくする
                # 1.2 → 20%大きくする
                note.velocity = min(127, int(note.velocity * 1.1))

                # 音の開始時間をランダムにずらす
                #
                # -0.01～0.01秒の範囲でズレる。
                # 数字を大きくするとズレが大きくなる。
                random_shift = random.uniform(-0.01, 0.01)

                # 0秒より前にならないようにする
                note.start = max(0, note.start + random_shift)


    # 変換後のMIDIを返す
    return midi


# ==============================
# 単体で動作確認する場合
# ==============================

if __name__ == "__main__":

    input_path = "test.mid"

    converted_midi = transform_midi(
        input_path,
        style="musicbox"
    )

    converted_midi.write("test_output.mid")

    print("変換が完了しました。")