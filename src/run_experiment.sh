#!/usr/bin/env bash

module add python36-modules-gcc
python3.6 -m venv .venv
source .venv/bin/activate

pip3.6 install -r requirements.txt
echo "Packages installed!"

HOME="~"
PERO_PATH=$HOME"/code_from_others/pero/"
PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
export PATH=$PATH:$PYTHONPATH

SCRIPT=$HOME"/code_from_others/pero/pytorch_ctc/train_pytorch_ocr.py"
LENGTH=1700
LMDB=$HOME"/datasets/images.lmdb"
#NET=NET_SIMPLE_BC_3_BLC_2_BFC_24
#NET=NET_RES_D3_BFC_24_BN
#NET=NET_RES_D3_BFC_24_MI
NET=VGG_LSTM_B64_L17_S4_CB4

DATA_TYPE=all
TRANSFORMER=
#'--data-manipulator UNIVERSAL_PRINT'
START='--start-iteration 20700'


python3.6 -u $SCRIPT $START  \
    --trn-data data.trn \
    --tst-data data.tst \
    -l $LMDB \
    -n $NET $TRANSFORMER \
    --max-line-width ${LENGTH} --max-iterations 700000 \
    --max-buffer-size=1024000000 --max-buffered-lines=10000 \
    --dropout-rate 0.05 --learning-rate 0.0001 --batch-size 24  --view-step 500  \
    --test --checkpoint-dir checkpoints -c all \
    --show-trans --test --warm-up-iterations 500 2>&1 | tee -a log_x.txt

