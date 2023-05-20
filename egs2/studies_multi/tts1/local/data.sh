#!/usr/bin/env bash

set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0

stage=-1
stop_stage=2
# spk=jvs010
spk=ITA

log "$0 $*"
. utils/parse_options.sh

if [ $# -ne 0 ]; then
    log "Error: No positional arguments are required."
    exit 2
fi

. ./path.sh || exit 1;
. ./cmd.sh || exit 1;
. ./db.sh || exit 1;

# if [ -z "${JVS}" ]; then
#    log "Fill the value of 'JVS' of db.sh"
#    exit 1
# fi
# db_root=${JVS}
db_root=/autofs/diamond2/share/corpus/STUDIES/STUDIES

train_set=${spk}_tr_no_dev
train_dev=${spk}_dev
eval_set=${spk}_eval1

if [ ${stage} -le -1 ] && [ ${stop_stage} -ge -1 ]; then
    log "stage -1: local/data_download.sh"
    local/data_download.sh "${db_root}"
fi

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
    log "stage 0: local/data_prep.sh"
    # local/data_prep.sh "${db_root}"/jvs_ver1 "${spk}" "data/${spk}"
    local/data_prep.sh "${db_root}" "${spk}" "data/${spk}"
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    log "stage 2: utils/subset_data_dir.sh"
    # # make evaluation and devlopment sets
    # utils/copy_data_dir.sh "data/${spk}_parallel100" "data/${train_set}"
    # utils/subset_data_dir.sh --first "data/${spk}_nonpara30" 15 "data/${train_dev}"
    # utils/subset_data_dir.sh --last "data/${spk}_nonpara30" 15 "data/${eval_set}"

    # 感情音声はすべて学習に使いたいので，そうする
    # 一方で dev にもある程度入れておかないと，最良モデルパラメタを取得する部分がおかしくなりそうなので，
    # 最初の5文ずつ（計20文）を dev に入れる．
    # そのほか，Recitation324の最後の24文のうち，最初の12文をdev，後半12文をevalにする．

    utils/subset_data_dir.sh --first "data/${spk}_Emotion100-Normal" 5 "data/${spk}_Emotion100-Normal_5"
    utils/subset_data_dir.sh --first "data/${spk}_Emotion100-Happy" 5 "data/${spk}_Emotion100-Happy_5"
    utils/subset_data_dir.sh --first "data/${spk}_Emotion100-Angry" 5 "data/${spk}_Emotion100-Angry_5"
    utils/subset_data_dir.sh --first "data/${spk}_Emotion100-Sad" 5 "data/${spk}_Emotion100-Sad_5"
    utils/subset_data_dir.sh --first "data/${spk}_Recitation324" 300 "data/${spk}_Recitation324_300"
    utils/subset_data_dir.sh --last  "data/${spk}_Recitation324" 24 "data/${spk}_Recitation324_last24"
    utils/subset_data_dir.sh --first "data/${spk}_Recitation324_last24" 12 "data/${spk}_Recitation324_last24_dev"
    utils/combine_data.sh "data/${train_set}" \
        "data/${spk}_Emotion100-Normal" \
        "data/${spk}_Emotion100-Happy" \
        "data/${spk}_Emotion100-Angry" \
        "data/${spk}_Emotion100-Sad" \
        "data/${spk}_Recitation324_300"
    utils/combine_data.sh "data/${train_dev}" \
        "data/${spk}_Emotion100-Normal_5" \
        "data/${spk}_Emotion100-Happy_5" \
        "data/${spk}_Emotion100-Angry_5" \
        "data/${spk}_Emotion100-Sad_5" \
        "data/${spk}_Recitation324_last24_dev"
    utils/subset_data_dir.sh --last  "data/${spk}_Recitation324_last24" 12 "data/${eval_set}"
fi

log "Successfully finished. [elapsed=${SECONDS}s]"
