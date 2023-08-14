#!/usr/bin/env bash
# Author: Vojtěch Vlach
# Contact: xvlach22@vutbr.cz

BP_GIT_EXP="$HOME/BP_sequel/bp-git/experiments"
SCRIPT=$BP_GIT_EXP"/evaluate_checkpoints.py"
NAME=`basename $(pwd)`
OUTPUT_FOLDER=evaluated_checkpoints/
TXT_OUT=$OUTPUT_FOLDER/$NAME".txt"
mkdir -p $OUTPUT_FOLDER
touch $TXT_OUT

echo "============== Running evaluation script =============="

python $SCRIPT \
    --input-files checkpoints/checkpoint_*.pth.out \
    --ground-truths checkpoints/ground_truth*.tst_out \
    --output-folder $OUTPUT_FOLDER \
    --name $NAME | tee $TXT_OUT
