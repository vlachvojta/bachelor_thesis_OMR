#!/usr/bin/env bash
#PBS -l select=1:ncpus=1:ngpus=1:mem=15gb:scratch_local=10gb:cluster=black
#PBS -q gpu@cerit-pbs.cerit-sc.cz
#PBS -l walltime=2:0:0
#PBS -m abe
#PBS -N 230123_sagnostic_WER_test

# export EXPERIMENT="230123_sagnostic_WER_test"
# NGPU=1

# echo "SCRATCH: "$SCRATCH
# cd $SCRATCH
# cp -r /storage/brno2/home/xvlach22/bp_omr/datasets $SCRATCH/datasets
# mkdir $SCRATCH/experiments
# cp -r /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT $SCRATCH/experiments/$EXPERIMENT
# cp -r /storage/brno2/home/xvlach22/bp_omr/ubuntu_fonts $SCRATCH/ubuntu_fonts
# cp -r /storage/brno2/home/xvlach22/bp_omr/code_from_others $SCRATCH/code_from_others
# cp -r /storage/brno2/home/xvlach22/bp_omr/bp-git $SCRATCH/bp-git
# cd experiments/$EXPERIMENT
# trap 'cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/ ; echo "data saved back to storage" ; clean_scratch' EXIT TERM

module add python36-modules-gcc

pip3.6 install --upgrade pip 1>/dev/null

HOME=$HOME"/bp_omr/"
# PERO_PATH=$HOME"/code_from_others/pero/"
# PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
BP_GIT_EXP=$HOME"/bp-git/src/experiments"
# export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH:$BP_GIT_EXP
export PYTHONPATH=$BP_GIT_EXP
export PATH=$PATH:$PYTHONPATH

SCRIPT=$BP_GIT_EXP"/evaluate_checkpoints.py"
NAME=`basename $(pwd)`

# SCRIPT=$HOME"/code_from_others/pero/pytorch_ctc/train_pytorch_ocr.py"
# LENGTH=1700
# LMDB=$HOME"/datasets/images.lmdb"
# DATA_TRN=$HOME"/datasets/data_SSemantic.trn"
# DATA_TST=$HOME"/datasets/data_SSemantic.tst"
# NET=VGG_LSTM_B64_L17_S4_CB4

# DATA_TYPE=all
# TRANSFORMER=
# START_ITER=`python3 $GET_LAST_POINT_PY checkpoints/`
# START="--start-iteration 0"$START_ITER
# FONT=$HOME/"ubuntu_fonts/Ubuntu-Regular.ttf"

# pip3.6 install arabic-reshaper 1>/dev/null
# pip3.6 install lmdb 1>/dev/null
# pip3.6 install safe-gpu 1>/dev/null
# pip3.6 install shapely imgaug lxml Levenshtein rapidfuzz typing-extensions 1>/dev/null
pip3.6 install jiwer 1>/dev/null
# pip3.6 install torchvision==0.2.2 1>/dev/null
# echo "python modules installed"
# pwd
echo "============== Running evaluation script =============="

python3.6 $SCRIPT \
    --input-files checkpoints/checkpoint_*.pth.tst_out \
    --ground-truth checkpoints/ground_truth.tst_out \
    --output-folder evaluated_checkpoints \
    --name $NAME

# cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/
# clean_scratch
# exit
