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
echo "Matching images and labels using matchmaker.py"
echo "================================================"
echo ""


# ================================ MAIN ================================

mkdir -p $out_dir

python $BP_GIT/musescore-dataset-utilities/matchmaker.py \
    --image-folder $in_dir_images \
    --label-files $in_dir_labels/0_labels.semantic \
    --output-folder $out_dir
