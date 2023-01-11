#!/usr/bin/env bash
#PBS -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_local=20gb:cluster=grimbold
#PBS -q gpu
#PBS -N 230112_first_auto_try
#PBS -l walltime=0:30:0
#PBS -m abe

export EXPERIMENT="230112_first_auto_try"
echo "SCRATCH: "$SCRATCH
cd $SCRATCH
cp -r /storage/brno2/home/xvlach22/bp_omr/datasets $SCRATCH/datasets
mkdir $SCRATCH/experiments
cp -r /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT $SCRATCH/experiments/$EXPERIMENT
cp -r /storage/brno2/home/xvlach22/bp_omr/ubuntu_fonts $SCRATCH/ubuntu_fonts
cp -r /storage/brno2/home/xvlach22/bp_omr/code_from_others $SCRATCH/code_from_others
cd experiments/$EXPERIMENT
# chmod u+x run_experiment.sh
trap 'cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/scratch_copy ; clean_scratch' EXIT TERM
module add python36-modules-gcc

pip3.6 install --upgrade pip 1>/dev/null
# pip3.6 install -r pero_requirements.txt 1>/dev/null

HOME=$SCRATCH
PERO_PATH=$HOME"/code_from_others/pero/"
PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
export PATH=$PATH:$PYTHONPATH

SCRIPT=$HOME"/code_from_others/pero/pytorch_ctc/train_pytorch_ocr.py"
LENGTH=1700
LMDB=$HOME"/datasets/images.lmdb"
DATA_TRN=$HOME"/datasets/data.trn"
DATA_TST=$HOME"/datasets/data.tst"
#NET=NET_SIMPLE_BC_3_BLC_2_BFC_24
#NET=NET_RES_D3_BFC_24_BN
#NET=NET_RES_D3_BFC_24_MI
NET=VGG_LSTM_B64_L17_S4_CB4

DATA_TYPE=all
TRANSFORMER=
#'--data-manipulator UNIVERSAL_PRINT'
START='' # '--start-iteration 20700'
FONT=$HOME/"ubuntu_fonts/Ubuntu-Regular.ttf"

pip3.6 install arabic-reshaper 1>/dev/null
pip3.6 install lmdb 1>/dev/null
pip3.6 install safe-gpu 1>/dev/null
pip3.6 install shapely imgaug lxml Levenshtein rapidfuzz typing-extensions 1>/dev/null
# pip3.6 install nvidia-cublas-cu11 1>/dev/null
# pip3.6 install nvidia-cudnn-cu11 1>/dev/null
# pip3.6 install nvidia-cuda-nvrtc-cu11 1>/dev/null
# pip3.6 install nvidia-cuda-runtime-cu11 1>/dev/null
pip3.6 install torchvision==0.2.2 1>/dev/null
# pip3.6 install torch==1.8.0+cu111 torchvision==0.2.2+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
echo "python modules installed"
echo "============== Running training script =============="

python3.6 -u $SCRIPT $START  \
    --trn-data $DATA_TRN \
    --tst-data $DATA_TST \
    -l $LMDB \
    -n $NET $TRANSFORMER \
    --max-line-width ${LENGTH} --max-iterations 700000 \
    --max-buffer-size=1024000000 --max-buffered-lines=10000 \
    --dropout-rate 0.05 --learning-rate 0.0001 --batch-size 24  --view-step 500  \
    --test --checkpoint-dir checkpoints -c all \
    --font $FONT \
    --show-trans --test --warm-up-iterations 500 2>&1 | tee -a log_x.txt
