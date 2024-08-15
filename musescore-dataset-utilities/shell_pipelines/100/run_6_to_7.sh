#!/bin/bash

# get location of this script
EXPERIMENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# if $BP_GIT variable is not set, default to current directory
if [ -z $BP_GIT ]; then
    BP_GIT="./"
fi

# ================================ PARAMETERS ================================
# Return default value if argument is empty
get_arg() {
    if [ -z "$1" ]; then
        echo $2 # return default value
    else
        echo $1 # return argument value
    fi
}

in_dir=$(get_arg $1 '6_copied_pairs')
out_dir=$(get_arg $2 '7_lmdb_db')

echo ""
echo "================================================"
echo "Running 100/run_6_to_7.sh"
echo "Matching images and labels using matchmaker.py"
echo "================================================"
echo ""


# ================================ MAIN ================================

mkdir -p $out_dir

python $BP_GIT/dataset-utilities/lmdb_generator.py \
    --src-folders $in_dir \
    --output-folder $out_dir \
    --extensions-text 'semantic' \
    --extensions-images 'png' \
    --ignore-texts

python $BP_GIT/dataset-utilities/symbol_converter.py \
    --input_files $in_dir/0_labels.semantic \
    --output_file $out_dir/0_labels.semantic \
    --translator $BP_GIT/dataset-utilities/translator.Semantic_to_SSemantic.json \
    --mode matchmaker

# - label_set_splitter.py - split whole label file to two randomized sets of labels for validation set and training set
