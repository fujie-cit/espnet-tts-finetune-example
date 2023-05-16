#!/usr/bin/env python3

# 転記ファイル（transcription_file.txt）と音声リストファイル（wav.scp）の内容を読み込み
# 音声合成の学習のためのテキスト一覧のファイルを作成する.
#
# 例
# 1. transcription_file.txt
#    講師|喜び|えっ、嘘でしょ？|エッ、ウソデショ？
#    講師|喜び|シュヴァイツァーは見習うべき人間です。|シュヴァイツァーワミナラウベキニンゲンデス。
#    講師|喜び|デーヴィスさんはとても疲れているように見える。|デーヴィスサンワトテモツカレテイルヨーニミエル。
#    講師|喜び|スティーヴはジェーンから手紙をもらった。|スティーヴワジェーンカラテガミヲモラッタ。
#    講師|喜び|彼女はモーツァルトやベートーヴェンといった、古典派の作曲家が好きだ。|カノジョワモーツァルトヤベートーヴェントイッタ、コテンハノサッキョクカガスキダ。
# 2. wav.scp
#    ITA_ITA-Emotion100-Teacher-Happy-001 /somewhere/wav/ITA-Emotion100-Teacher-Happy-001.wav
#    ITA_ITA-Emotion100-Teacher-Happy-002 /somewhere/wav/ITA-Emotion100-Teacher-Happy-002.wav
#    ITA_ITA-Emotion100-Teacher-Happy-003 /somewhere/wav/ITA-Emotion100-Teacher-Happy-003.wav
#    ITA_ITA-Emotion100-Teacher-Happy-004 /somewhere/wav/ITA-Emotion100-Teacher-Happy-004.wav
#    ITA_ITA-Emotion100-Teacher-Happy-005 /somewhere/wav/ITA-Emotion100-Teacher-Happy-005.wav
# というファイル内容が与えられた場合は以下を標準出力に出す
#    ITA_ITA-Emotion100-Teacher-Happy-001 えっ、嘘でしょ？
#    ITA_ITA-Emotion100-Teacher-Happy-002 シュヴァイツァーは見習うべき人間です。
#    ITA_ITA-Emotion100-Teacher-Happy-003 デーヴィスさんはとても疲れているように見える。
#    ITA_ITA-Emotion100-Teacher-Happy-004 スティーヴはジェーンから手紙をもらった。
#    ITA_ITA-Emotion100-Teacher-Happy-005 彼女はモーツァルトやベートーヴェンといった、古典派の作曲家が好きだ。
# 
#  このファイルの実行は以下のように行う
#  $ python make_text.py transcription_file.txt wav.scp > text

import sys

def main(transcription_file, wav_scp_file):
    with open(transcription_file, "r", encoding="utf-8") as tf, open(wav_scp_file, "r", encoding="utf-8") as wf:
        transcriptions = [line.strip().split("|")[-2] for line in tf]
        wav_ids = [line.strip().split()[0] for line in wf]

        if len(transcriptions) != len(wav_ids):
            raise ValueError("The number of lines in the transcription file and wav.scp file do not match.")

        for wav_id, transcription in zip(wav_ids, transcriptions):
            print(f"{wav_id} {transcription}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_text.py transcription_file.txt wav.scp")
        sys.exit(1)

    transcription_file = sys.argv[1]
    wav_scp_file = sys.argv[2]

    main(transcription_file, wav_scp_file)




