# ESPnet関係のメモ

##  モデルをアップロードする方法

- 予め HuggingFace にリポジトリを作成する
- ```git lfs install```を実行しておく（git lfs がインストールされている必要がある）
- Stage 8 から動作させる．このとき
  - `--skip_upload_hf false` にする
  - `--hf_repo` に作成したリポジトリを指定する
- アップロード時にユーザ名とパスワードを聞かれるので入力する
- アップロードに失敗した場合は，一度ローカルのリポジトリ（```./exp/hf_*```）は削除した方がよさそう．

**実行例**
```
$ ./run.sh \
    --stage 8 \
    --g2p pyopenjtalk_prosody \
    --min_wav_duration 0.38 \
    --fs 22050 \
    --n_fft 1024 \
    --n_shift 256 \
    --dumpdir dump/22k \
    --win_length null \
    --tts_task gan_tts \
    --feats_extract linear_spectrogram \
    --feats_normalize none \
    --train_config ./conf/tuning/finetune_vits.yaml \
    --train_args "--init_param ${PRETRAINED_MODEL_FILE}" \
    --tag finetune_vits_raw_phn_jaconv_pyopenjtalk_prosody \
    --inference_model train.total_count.ave_10best.pth \
    --skip_upload_hf false \
    --hf_repo fujie/fujie_studies_tts_finetune_vits_raw_phn_jaconv_pyopenjtalk_prosody
```

## ESPnetの拡張について

特殊トークンを扱えるようにするための工夫

### トークナイザの拡張

https://github.com/fujie-cit/espnet/commit/8f3fcc4654cd85df5156cd0444a330d5470582be

`espnet/espnet2/text/phoneme_tokenizer.py` に，`pyopenjtalk_prosody_with_special_token` を追加しました．

### 事前学習読み込みの拡張

https://github.com/fujie-cit/espnet/commit/be628f2508935c07a0b4640cdd0e62a35476cf09

埋め込み層のパラメータの読み込み時に限り，サイズの違うパラメータを読み込めるようにしました．
