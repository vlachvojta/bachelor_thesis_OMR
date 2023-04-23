#!/usr/bin/env bash

root=`cd ~ && pwd`
BP_GIT_EXP="$root/skola/BP/bp-git/src/experiments"

SCRIPT=$BP_GIT_EXP"/evaluate_checkpoints.py"
NAME=`basename $(pwd)`
OUTPUT_FOLDER=evaluated_checkpoints/
TXT_OUT=$OUTPUT_FOLDER/$NAME".txt"
mkdir -p $OUTPUT_FOLDER
touch $TXT_OUT

echo "============== Running evaluation script =============="

python3.8 $SCRIPT \
    --input-files checkpoints/checkpoint_*.tst_out \
    --ground-truths checkpoints/ground_truth*.tst_out \
    --output-folder $OUTPUT_FOLDER \
    --name $NAME | tee $TXT_OUT
