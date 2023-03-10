#!/usr/bin/env bash

HOME=$HOME"/bp_omr/"
BP_GIT_EXP=$HOME"/bp-git/src/experiments"

export PYTHONPATH=$BP_GIT_EXP
export PATH=$PATH:$PYTHONPATH

SCRIPT=$BP_GIT_EXP"/evaluate_checkpoints.py"
NAME=`basename $(pwd)`
OUTPUT_FOLDER=evaluated_checkpoints/
TXT_OUT=$OUTPUT_FOLDER/$NAME".txt"
mkdir -p $OUTPUT_FOLDER
touch $TXT_OUT

module add python36-modules-gcc
pip3.6 install --upgrade pip 1>/dev/null
pip3.6 install jiwer 1>/dev/null

echo "============== Running evaluation script =============="

python3.6 $SCRIPT \
    --input-files checkpoints/checkpoint_*.pth.tst_out \
    --ground-truth checkpoints/ground_truth.tst_out \
    --output-folder $OUTPUT_FOLDER \
    --name $NAME | tee $TXT_OUT
