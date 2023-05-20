from espnet2.bin.tts_inference import Text2Speech
import os

# 実験ディレクトリのパス
exp_dir = "./exp/tts_finetune_vits_raw_phn_jaconv_pyopenjtalk_prosody_with_special_token"

# 学習設定ファイルのパス
train_config_path = os.path.join(exp_dir, "config.yaml")

# モデルファイルのパス
# model_path = os.path.join(exp_dir, "train.total_count.best.pth")
model_path = os.path.join(exp_dir, "latest.pth")

# ボコーダモデルの名前
vocoder_tag = "parallel_wavegan/jsut_parallel_wavegan.v1"

# text2speechインスタンスの作成
text2speech = Text2Speech.from_pretrained(
    train_config=train_config_path,
    model_file=model_path,
    vocoder_tag=vocoder_tag,
)

# テキストから音声を生成
text = "<happy>あらゆる現実を、すべて自分の方へ捻じ曲げたのだ。"
speech = text2speech(text)

# 合成結果のファイルへの保存                                                                                                                                                                                                  
import soundfile as sf
sf.write("test_gen.wav", speech["wav"], text2speech.fs, "PCM_16")
