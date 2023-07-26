#!/usr/bin/env bash

EXPERIMENT="0_local_decode_pth"

# module add python36-modules-gcc
# pip3 install --upgrade pip
# pip3 install safe_gpu lmdb opencv-python scipy brnolm
# pip3 install torch lmdb safe_gpu brnolm torchvision pero_ocr

home=$HOME"/BP_sequel/"
source $home"/pero_venv/bin/activate"
PERO_PATH=$home"/PERO"
# PERO_OCR_PATH=$home"/code_from_others/pero-ocr"
# export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
# export PATH=$PATH:$PYTHONPATH

# Dataset
LMDB=$home"/datasets/musescore/mashup_115k_with_hard/images.lmdb"
DATA_TST=$home"/datasets/musescore/mashup_115k_with_hard/data_head_10.SSemantic.tst"

# Python scripts
# EXPORT_PY=$PERO_PATH"/pytorch_ctc/export_model.py"
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"
DECODE_PY=$PERO_PATH"/karelb-ocr-scripts/decode_logits.py"

# Python script arguments
NET={"dim_model":512,"dim_ff":2048,"heads":8,"dropout_rate":0.05,"encoder_layers":4,"decoder_layers":4}
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
        echo "----runnning get_folder_logits.py----"
        python3 $GET_LOGITS_PY  \
            --ocr-json $OCR_JSON \
            --model-type 'Pytorch-Transformer' \
            --input $LMDB  \
            --lines $DATA_TST \
            --output $PICKLE

        echo
        echo "----runnning decode_logtis.py----"
        python3 "$DECODE_PY" \
            --ocr-json "$OCR_JSON" \
            --input "$PICKLE" \
            --report-eta --best $checkpoint.out --greedy \
            --confidence $CONFIDENCE
        echo
        echo "This checkpoint took: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
    fi
done
