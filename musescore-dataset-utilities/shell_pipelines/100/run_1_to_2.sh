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

in_dir=$(get_arg $1 '1_musicxml_by_M3_CLI')
out_dir=$(get_arg $2 '2_musicxml_parts')

echo ""
echo "================================================"
echo "Running 100/run_1_to_2.sh"
echo "musicxml -> musicxml parts using part_splitter.py"
echo "================================================"
echo ""

# ================================ MAIN ================================

mkdir -p $out_dir

# Split parts
python $BP_GIT/musescore-dataset-utilities/part_splitter.py \
    --input-folder $in_dir \
    --output-folder $out_dir \
    --staves-on-page 1


