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

in_dir=$(get_arg $1 '3_img_pages')
out_dir=$(get_arg $2 '4_img_staves')

echo ""
echo "================================================"
echo "png pages -> png staves using img_to_staves.py"
echo "================================================"
echo ""


# ================================ MAIN ================================

mkdir -p $out_dir

# Split parts
python $BP_GIT/musescore-dataset-utilities/img_to_staves.py \
    --input-folder $in_dir \
    --output-folder $out_dir \
    --staff-count 1


