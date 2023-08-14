#!/usr/bin/env bash

EXPERIMENT=`basename $(pwd)`

home=$HOME"/BP_sequel/"
# source $home"/pero_venv/bin/activate"  # Activate pero virtual environment
PERO_PATH=$home"/PERO-DCGM"
PERO_OCR_PATH=$home"/lib/PERO_OCR"
export PYTHONPATH=$PERO_OCR_PATH

# Data
LMDB=$home"/datasets/deploy/musescore/mashup_115k_with_hard/images.lmdb"
LINES=$home"/experiments/"$EXPERIMENT"/data_head_10.SSemantic.tst"

# Python scripts
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"

# Python script arguments
CHECKPOINT_PATH=$home"/experiments/"$EXPERIMENT"/checkpoints/"
OCR_JSON=$home"/experiments/"$EXPERIMENT"/ocr.json"

for checkpoint in `ls -r $CHECKPOINT_PATH/checkpoint_*.pth`; do
    SECONDS=0  # start meassuring time
    echo ""
    echo "=================================== $checkpoint"
    if [ -f $checkpoint.out ]; then
        echo "File $checkpoint.out already exists"
    else
        echo
        echo "----runnning get_folder_logits.py----"
        echo
        python3 $GET_LOGITS_PY \
            --ocr-json $OCR_JSON \
            --model-type 'Pytorch-Transformer' \
            --input $LMDB  \
            --lines $LINES \
            --transcriptions $checkpoint.out

        echo
        echo "This checkpoint took: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
    fi
done
