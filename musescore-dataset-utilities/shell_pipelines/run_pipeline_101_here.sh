#!/bin/bash

# Description: Place this script to your folder for easy access to pipeline 100
# Usage: ./run_pipeline_100_here.sh [<sub_dir>]

# if $BP_GIT variable is not set, default to current directory
if [ -z $BP_GIT ]; then
    echo "BP_GIT variable not set. Set it to find pipeline"
    exit
fi

# ================================ PARAMETERS ================================
get_arg() {
    if [ -z "$1" ]; then
        echo $2 # return default value
    else
        echo $1 # return argument value
    fi
}

sub_dir=$(get_arg $1 '')

# ================================ MAIN ================================

$BP_GIT/musescore-dataset-utilities/shell_pipelines/run_pipeline_101.sh './' $sub_dir  | tee -a pip_101_$sub_dir.log
