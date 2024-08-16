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

in_dir_images=$(get_arg $1 '4_img_staves')
in_dir_labels=$(get_arg $2 '5_labels_semantic')
out_dir=$(get_arg $3 '6_copied_pairs')

echo ""
echo "================================================"
echo "Running 100/run_5_to_6.sh"
echo "Matching images and labels using check_staff_lines.py, matchmaker.py and symbol_converter.py"
echo "================================================"
echo ""


# ================================ MAIN ================================

python $BP_GIT/musescore-dataset-utilities/check_staff_lines.py \
    --input-dir $in_dir_images \
    --output-dir $in_dir_images/checking_staff_lines \
    --save-images

mkdir -p $out_dir

python $BP_GIT/musescore-dataset-utilities/matchmaker.py \
    --image-folder $in_dir_images \
    --label-files $in_dir_labels/0_labels.semantic \
    --output-folder $out_dir

python $BP_GIT/dataset-utilities/symbol_converter.py \
    --translator $BP_GIT/translators/translator.Semantic_to_SSemantic.json \
    --input_files $out_dir/0_labels.semantic \
    --output_file $out_dir/0_labels.SSemantic \
    --mode matchmaker \
