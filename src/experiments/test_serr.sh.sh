#!/usr/bin/env bash

EXPERIMENT="230124_sagnostic_counting_serr"
cd $SCRATCH
echo "SCRATCH: "$SCRATCH
cp -r /storage/brno2/home/xvlach22/bp_omr/datasets $SCRATCH/datasets
mkdir $SCRATCH/experiments
cp -r /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT $SCRATCH/experiments/$EXPERIMENT
cp -r /storage/brno2/home/xvlach22/bp_omr/ubuntu_fonts $SCRATCH/ubuntu_fonts
cp -r /storage/brno2/home/xvlach22/bp_omr/code_from_others $SCRATCH/code_from_others
cd experiments/$EXPERIMENT
# chmod u+x run_experiment.sh

module add python36-modules-gcc
pip3.6 install --upgrade pip 1>/dev/null

HOME=$SCRATCH
PERO_PATH=$HOME"/code_from_others/pero"
PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
export PATH=$PATH:$PYTHONPATH

# Dataset
LMDB=$HOME"/datasets/images.lmdb"
DATA_TST=$HOME"/datasets/data_2.tst" # data_2.tst: SAgnostic, data.tst: SSemantic

# Python scripts
EXPORT_PY=$PERO_PATH"/pytorch_ctc/export_model.py"
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"
DECODE_PY=$PERO_PATH"/karelb-ocr-scripts/decode_logits.py"

# Python script arguments
NET=VGG_LSTM_B64_L17_S4_CB4
CHECKPOINT="checkpoint_050500.pth"
CHECKPOINT_PATH=$HOME"/experiments/"$EXPERIMENT"/checkpoints/"
OCR_JSON=$CHECKPOINT_PATH"/out.json"
OCR_MODEL=$CHECKPOINT_PATH"/out.pt"
PICKLE=$CHECKPOINT_PATH"/pickle_out.pkl"
DECODED=$CHECKPOINT_PATH$CHECKPOINT".out"

pip3.6 install safe_gpu lmdb opencv-python scipy brnolm 1>/dev/null
pip3.6 install torchvision==0.2.2 1>/dev/null

# Run scripts
echo "====runnning export_model.py===="
python3.6 -u $EXPORT_PY  \
    --path $CHECKPOINT_PATH$CHECKPOINT --net $NET  \
    --line-height 100 --line-vertical-scale 2705  \
    --output-json-path $OCR_JSON \
    --output-model-path $OCR_MODEL  \
    --trace

echo "====runnning get_folder_logits.py===="
python3.6 -u $GET_LOGITS_PY  \
    --ocr-json $OCR_JSON  --input $LMDB  \
    --lines $DATA_TST  --output $PICKLE

echo "====runnning decode_logtis.py===="
python3.6 -u $DECODE_PY \
    --ocr-json $OCR_JSON \
    --input $PICKLE \
    --report-eta --best $DECODED --greedy \
    --confidence $CHECKPOINT_PATH"/del.confidence"
# What do you mean WHERE (with best and confidence args)

# TODO evaluate $DECODED with $DATA_TST