#!/usr/bin/env python3

# 転記ファイル（transcription_file.txt）と音声リストファイル（wav.scp）の内容を読み込み
# 音声合成の学習のためのテキスト一覧のファイルを作成する.
#
# 例
# 1. transcription_file.txt
#    講師|喜び|えっ、嘘でしょ？|エッ、ウソデショ？
#    講師|怒り|シュヴァイツァーは見習うべき人間です。|シュヴァイツァーワミナラウベキニンゲンデス。
#    講師|悲しみ|デーヴィスさんはとても疲れているように見える。|デーヴィスサンワトテモツカレテイルヨーニミエル。
#    講師|平静|スティーヴはジェーンから手紙をもらった。|スティーヴワジェーンカラテガミヲモラッタ。
#    講師|喜び|彼女はモーツァルトやベートーヴェンといった、古典派の作曲家が好きだ。|カノジョワモーツァルトヤベートーヴェントイッタ、コテンハノサッキョクカガスキダ。
# 2. wav.scp
#    ITA_ITA-Emotion100-Teacher-Happy-001 /somewhere/wav/ITA-Emotion100-Teacher-Happy-001.wav
#    ITA_ITA-Emotion100-Teacher-Happy-002 /somewhere/wav/ITA-Emotion100-Teacher-Happy-002.wav
#    ITA_ITA-Emotion100-Teacher-Happy-003 /somewhere/wav/ITA-Emotion100-Teacher-Happy-003.wav
#    ITA_ITA-Emotion100-Teacher-Happy-004 /somewhere/wav/ITA-Emotion100-Teacher-Happy-004.wav
#    ITA_ITA-Emotion100-Teacher-Happy-005 /somewhere/wav/ITA-Emotion100-Teacher-Happy-005.wav
# というファイル内容が与えられた場合は以下を標準出力に出す
#    ITA_ITA-Emotion100-Teacher-Happy-001 [Happy]えっ、嘘でしょ？
#    ITA_ITA-Emotion100-Teacher-Happy-002 [Angry]シュヴァイツァーは見習うべき人間です。
#    ITA_ITA-Emotion100-Teacher-Happy-003 [Sad]デーヴィスさんはとても疲れているように見える。
#    ITA_ITA-Emotion100-Teacher-Happy-004 スティーヴはジェーンから手紙をもらった。
#    ITA_ITA-Emotion100-Teacher-Happy-005 [Happy]彼女はモーツァルトやベートーヴェンといった、古典派の作曲家が好きだ。
# 
#  このファイルの実行は以下のように行う
#  $ python make_text.py transcription_file.txt wav.scp > text
import sys

def create_text(transcription_file_path, wav_scp_path):
    with open(transcription_file_path, 'r') as transcription_file:
        transcription_lines = transcription_file.readlines()

    with open(wav_scp_path, 'r') as wav_file:
        wav_lines = wav_file.readlines()

    emotions = {
        '喜び': '<happy>',
        '悲しみ': '<sad>',
        '怒り': '<angry>'
    }

    for i, line in enumerate(wav_lines):
        line = line.strip()
        if line:
            parts = line.split(' ')
            key = parts[0]
            wav_path = parts[1]
            if i < len(transcription_lines):
                transcription_line = transcription_lines[i].strip()
                parts = transcription_line.split('|')
                emotion = parts[1]
                transcription = parts[2].strip()

                if emotion in emotions:
                    emotion_label = emotions[emotion]
                    print(f"{key} {emotion_label}{emotion_label and ''}{transcription}")
                else:
                    print(f"{key} {transcription}")
            else:
                print(f"{key} {wav_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python make_text.py <transcription_file_path> <wav_scp_path>')
        sys.exit(1)

    transcription_file_path = sys.argv[1]
    wav_scp_path = sys.argv[2]
    create_text(transcription_file_path, wav_scp_path)

