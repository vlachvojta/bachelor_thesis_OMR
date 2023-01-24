#!/usr/bin/env bash

pwd
EXPERIMENT="230123_local_decode_pth"
# echo "SCRATCH: "$SCRATCH
# cd $SCRATCH
# cp -r /storage/brno2/home/xvlach22/bp_omr/datasets $SCRATCH/datasets
# mkdir $SCRATCH/experiments
# cp -r /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT $SCRATCH/experiments/$EXPERIMENT
# cp -r /storage/brno2/home/xvlach22/bp_omr/ubuntu_fonts $SCRATCH/ubuntu_fonts
# cp -r /storage/brno2/home/xvlach22/bp_omr/code_from_others $SCRATCH/code_from_others
# cd experiments/$EXPERIMENT
# chmod u+x run_experiment.sh

# module add python36-modules-gcc
pip3 install --upgrade pip
# pip3 install safe_gpu lmdb opencv-python scipy brnolm

HOME="/home/vlachvojta/skola/BP"
PERO_PATH=$HOME"/code_from_others/pero"
PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
export PATH=$PATH:$PYTHONPATH

# Dataset
LMDB=$HOME"/datasets/primus_full_converted_2_lmdb/images.lmdb"
DATA_TST=$HOME"/datasets/primus_full_converted_2_lmdb/data_2.tst"

# Python scripts
EXPORT_PY=$PERO_PATH"/pytorch_ctc/export_model.py"
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"
DECODE_PY=$PERO_PATH"/karelb-ocr-scripts/decode_logits.py"

# Python script arguments
NET=VGG_LSTM_B64_L17_S4_CB4
CHECKPOINT="checkpoint_030000.pth"
CHECKPOINT_PATH=$HOME"/experiments/"$EXPERIMENT"/checkpoints/"
OCR_JSON=$CHECKPOINT_PATH"/out.json"
OCR_MODEL=$CHECKPOINT_PATH"/out.pt"
PICKLE=$CHECKPOINT"/pickle_out.pkl"

# Run scripts
# echo "====runnning export_model.py===="
# python3 $EXPORT_PY  \
#     --path $CHECKPOINT_PATH$CHECKPOINT --net $NET  \
#     --line-height 100 --line-vertical-scale 2705  \
#     --output-json-path $OCR_JSON \
#     --output-model-path $OCR_MODEL  \
#     --trace --device cpu

echo "====runnning get_folder_logits.py===="
python3 $GET_LOGITS_PY  \
    --ocr-json $OCR_JSON  --input $LMDB  \
    --lines $DATA_TST  --output $PICKLE  \

echo "====runnning decode_logtis.py===="
python3 $DECODE_PY \
    --ocr-json $OCR_JSON \
    --input $PICKLE \
    --report-eta --best --confidence \
    --greedy
# What do you mean WHERE (with best and confidence args)
