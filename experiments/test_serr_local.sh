#!/usr/bin/env bash

#pwd
EXPERIMENT="0_local_decode_pth"

# module add python36-modules-gcc
# pip3 install --upgrade pip
# pip3 install safe_gpu lmdb opencv-python scipy brnolm
# pip3 install torch lmdb safe_gpu brnolm torchvision pero_ocr

home=$HOME"/BP_sequel/"
source ./.venv/bin/activate
PERO_PATH=$home"/PERO"
# PERO_OCR_PATH=$home"/code_from_others/pero-ocr"
# export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
# export PATH=$PATH:$PYTHONPATH

# Dataset
LMDB=$home"/datasets/primus_full_converted_2_lmdb/images.lmdb"
DATA_TST=$home"/datasets/primus_full_converted_2_lmdb/data_2.tst"

# Python scripts
EXPORT_PY=$PERO_PATH"/pytorch_ctc/export_model.py"
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"
DECODE_PY=$PERO_PATH"/karelb-ocr-scripts/decode_logits.py"

# Python script arguments
NET=VGG_LSTM_B64_L17_S4_CB4
CHECKPOINT_PATH=$home"/experiments/"$EXPERIMENT"/checkpoints/"
TMP=$home"/experiments/"$EXPERIMENT"/tmp/"
OCR_JSON=$TMP"out.json"
OCR_MODEL=$TMP"out.pt"
PICKLE=$TMP"/pickle_out.pkl"
CONFIDENCE=$TMP"/confidence.del"

for checkpoint in `ls -r $CHECKPOINT_PATH/checkpoint_*.pth`; do
    SECONDS=0  # start meassuring time
    echo ""
    echo "=================================== $checkpoint"
    if [ -f $checkpoint.out ]; then
        echo "File $checkpoint.out already exists"
    else
        echo
        echo "----runnning export_model.py----"
        python3 $EXPORT_PY  \
            --path $CHECKPOINT_PATH$checkpoint --net $NET  \
            --line-height 100 --line-vertical-scale 2705  \
            --output-json-path $OCR_JSON \
            --output-model-path $OCR_MODEL  \
            --trace --device cpu

        echo
        echo "----runnning get_folder_logits.py----"
        python3 $GET_LOGITS_PY  \
            --ocr-json $OCR_JSON  --input $LMDB  \
            --lines $DATA_TST  --output $PICKLE

        echo
        echo "----runnning decode_logtis.py----"
        python3 "$DECODE_PY" \
            --ocr-json "$OCR_JSON" \
            --input "$PICKLE" \
            --report-eta --best $checkpoint.out --greedy \
            --confidence $CONFIDENCE
        echo "This checkpoint took: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
    fi
done
