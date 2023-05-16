# ESPnet2 TTS のファインチューニングの実行例

## やりたいこと

- [STUDIESコーパス](https://research.nii.ac.jp/src/STUDIES.html)の一部を使って，感情を含む音声合成モデルを作成すること．
- 元となるモデルは，JSUTコーパスで事前学習済のVITSモデル https://huggingface.co/espnet/kan-bayashi_jsut_vits_prosody

## 参考資料

- https://github.com/espnet/espnet/tree/master/egs2/jvs/tts1

## 手順

### ESPnet2 の環境構築

```
$ git clone --depth 1 https://github.com/espnet/espnet.git -b v.202304
$ cd espnet/tools
$ . ./setup_cuda_env.sh /usr/local/cuda   # 環境によって異なる
$ ./setup_anaconda.sh
$ make
$ make pyopenjtalk.done
```

### レシピディレクトリの作成

```espnet/egs2```内の```jvs```ディレクトリを，```studies```という名前でコピーします．

（実行前に，ESPnetをクローンしたディレクトリに移動しておいてください．）

```
$ cp -r espnet/egs2/jvs espnet/egs2/studies
```

### 修正済ファイルのコピー

修正済みのファイルは，このリポジトリの ./egs2/studies/tts1/ にあるので，
それをコピーする．

```
$ cp -r egs2/studies/tts1/* espnet/egs2/studies/tts1/
```

どのように変更したかは付録で説明する．

### Stage 5までの実行

以降はレシピのディレクトリで実行するため，まず移動する．

```
$ cd espnet/egs2/studies/tts1/
```

トークンリストを作成するまでの前処理を実行する．

```
$ ./run.sh \
    --stage 0 \
    --stop-stage 5 \
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
    --train_config ./conf/tuning/finetune_vits.yaml
```

これで，```dump/22k/token_list/phn_jaconv_pyopenjtalk_prosody/tokens.txt```という名前でトークンリストが作成されるが，このリストはファインチューニングのために読み込む事前学習済モデルのトークンリストと異なるため，入れ替えが必要．

### 学習済モデルのダウンロード

学習済みのモデルを HuggingFace Hub からダウンロードする．

```
$ . ./path.sh
$ espnet_model_zoo_download --unpack true --cachedir downloads espnet/kan-bayashi_jsut_vits_prosody
```

ダウンロード先の確認をする．
それぞれ非常に長いパス名が表示されるが，一つずつ表示されればOK．

- 設定ファイル（config.yaml）の場所
    ```
    $ find downloads/ -name "config.yaml"
    downloads/models--espnet--kan-bayashi_jsut_vits_prosody/snapshots/3a859bfd2c9710846fa6244598000f0578a2d3e4/exp/tts_train_vits_raw_phn_jaconv_pyopenjtalk_prosody/config.yaml
    ```
- モデルファイル（*.pth）の場所
    ```
    $ find downloads/ -name "*.pth"
    downloads/models--espnet--kan-bayashi_jsut_vits_prosody/snapshots/3a859bfd2c9710846fa6244598000f0578a2d3e4/exp/tts_train_vits_raw_phn_jaconv_pyopenjtalk_prosody/train.total_count.ave_10best.pth
    ```

以降でこのパスをそれぞれ使うが，説明上長くなるので，以下のように環境変数に設定しておく．

```
$ export PRETRAINED_MODEL_CONFIG=`find downloads/ -name "config.yaml"`
$ export PRETRAINED_MODEL_FILE=`find downloads/ -name "*.pth"`
```

### トークンリストの修正

ダウンロードした事前学習済のモデルからトークンリストを作成する．

```
$ pyscripts/utils/make_token_list_from_config.py $PRETRAINED_MODEL_CONFIG 
```

できているか確認する．
これも先ほどと同様，非常に長いパス名が表示されるが，一つ表示されればOK．

```
$ find downloads/ -name "tokens.txt"
downloads/models--espnet--kan-bayashi_jsut_vits_prosody/snapshots/3a859bfd2c9710846fa6244598000f0578a2d3e4/exp/tts_train_vits_raw_phn_jaconv_pyopenjtalk_prosody/tokens.txt
```

これも長いため，環境変数に設定しておく．

```
$ export PRETRAINED_MODEL_TOKENS_TXT=`find downloads/ -name "tokens.txt"`
```

入れ替えを行います．

まず，古いファイルをバックアップします．

```
$ cp dump/22k/token_list/phn_jaconv_pyopenjtalk_prosody/tokens.txt{,.bak}
```

次に新しいファイルで古いファイルを上書きします．

```
$ cp $PRETRAINED_MODEL_TOKENS_TXT dump/22k/token_list/phn_jaconv_pyopenjtalk_prosody/tokens.txt
```

### ファインチューニング（Stage 6 以降）の実行

以上で準備が整ったので，Stage 6 以降の実際の学習を行います．
全てを終えるには数時間～数日かかります．

```
$ ./run.sh \
    --stage 6 \
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
    --tag finetune_vits_raw_phn_jaconv_pyopenjtalk_prosody
```

学習のログファイルは ```exp/tts_train_finetune_vits_raw_phn_jaconv_pyopenjtalk_prosody/train.log``` に出力されます．学習の進行状況はこのファイルを見ると分かります．

### 試しに音声を合成してみる

学習の途中でも数エポック学習が進行していれば，試しに音声を合成してみることができます．

学習と同様にレシピのディレクトリ（```espnet/egs2/studies/tts1```）で実行します．

まず ESPnet 用の Python 環境を有効にします．
```
$ . ../../../tools/activate_python.sh
```

初回は parallel_wavegan パッケージをインストールする必要があります．
```
$ pip install -U parallel_wavegan
```

合成用のテストプログラムを実行します．
```
$ test_gen.py
```

特に問題が無ければ、`test_gen.wav`が生成されます．

## 付録

### レシピ内のファイルの修正内容

#### run.sh の修正

```
spk=jvs010
```
を
```
spk=ITA
```
に修正しました（話者名をSTUDIESに合わせて変更）．

```
--local_data_opts "--spk ${spk}" \
```
を
```
--local_data_opts "--spk ${spk} --stage 0" \
```
に修正しました（データのダウンロードをスキップするため）．

#### local/make_text.py 

このファイルは新設のファイルです．

STUDIESの書き起こしファイルに合わせて data 内の text ファイルを生成するためのスクリプトです．

今回は，書き起こしに含まれる役名（講師）や感情（平静や喜び），およびそれらと転記テスト間の記号（`|`）は削除してtextとしています．
そのため，平静や喜びの音声がデータには含まれますが，それらの区別はつけません．

#### local/data_prep.sh の修正

- STUDIESの中で，`Emotion100-Happy`，`Emotion100-Normal`, `recitation324`を使用しています．
- 転記テキストの仕様が大きく違うため，`text`ファイルの生成には `local/make_text.py` を使用しています．
- コーパス上のラベルファイルの位置が異なるため，`segments`生成時の入力ファイルのパスを変更しました．

#### local/data.sh の修正

- `spk=jvs010`となっているところを`spk=ITA`に修正しました．
- `db.sh`を使わず，直接`db_root`に藤江研内のSTUDIESの位置を指定しています．
  - これはゆくゆく変更した方がよいと思います．
- Stage 2 におけるデータ分割の方法を変更しました．
  - 開発データは`Emotion100-Normal`の最初の15発話を使用しています．
  - 評価データは`Emotion100-Normal`の16発話目から30発話目の15発話を
  - 学習データはそれら以外全てとしています

#### conf/tuning/fintune_vits.yaml

- バッチサイズを小さくして比較的非力な計算機でも学習ができるようにしています．
  - 【参考】    
    ```
    batch_bins: 5000000       # batch bins (feats_type=raw)
    ```
    この値を小さくします．目安としては8GBのGPUを1枚を使う場合300000程度で動作を確認しました．
