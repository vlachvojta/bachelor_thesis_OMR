#!/usr/bin/env bash
export PYTHONPATH=/home/ihradis/projects/2018-01-15_PERO/pero-transformer:/home/ihradis/projects/2018-01-15_PERO/pero-transformer/src:/home/ihradis/projects/2018-01-15_PERO/pero-ocr-live

SCRIPT=/home/ihradis/projects/2018-01-15_PERO/pero-transformer/pytorch_ctc/train_pytorch_ocr.py
LMDB=/home/ihradis/projects/2018-01-15_PERO/data/HWR.2022-04-06/lmdb.hwr_40-1.0


NET='{"dim_model":512,"dim_ff":2048,"heads":8,"dropout_rate":0.05,"encoder_layers":4,"decoder_layers":4}'
DATA_TYPE=all
TRANSFORMER="--data-manipulator TRANSFORMER_HWR --max-line-width 1280"


python -u $SCRIPT $START  \
    --trn-data data.trn \
    --tst-data data.tst \
    --tst-data data.max-1000px.tst \
    -l $LMDB \
    $TRANSFORMER --loading-processes 4 \
    --model-type seq2seq --max-seq-len 600 --nonparam-fea-stage 0  -n "$NET"  \
    --max-iterations 700000 --warm-up-iterations 2000 \
    --max-buffer-size 1000000000 --max-buffered-lines 60000 \
    --dropout-rate 0.05 --learning-rate 0.0001 --batch-size 32 --view-step 1000  \
    --test --checkpoint-dir checkpoints -c all \
    --show-trans -t 2>&1 | tee -a log_test.txt












