#!/usr/bin/env bash

EXPERIMENT=`basename $(pwd)`

home=$HOME"/BP_sequel/"
# source $home"/pero_venv/bin/activate"  # Activate pero virtual environment
PERO_PATH=$home"/PERO-DCGM"
# PERO_OCR_PATH=$home"/lib/PERO_OCR"
# export PYTHONPATH=$PERO_OCR_PATH

# Data
LMDB="07_lines_lmdb/images.lmdb"
LINES="07_lines_lmdb/list.semantic"

# Python scripts
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"

# Python script arguments
CHECKPOINT_PATH=$home"/experiments/"$EXPERIMENT"/checkpoints/"
OCR_JSON="ocr.json"


python3 $GET_LOGITS_PY \
    --ocr-json $OCR_JSON \
    --model-type 'Pytorch-Transformer' \
    --input $LMDB  \
    --lines $LINES \
    --transcriptions "08_transcriptions/transcripted.ssemantic"
