#!/bin/bash

# get location of this script
EXPERIMENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# if $POLYPHONIC_OMR variable is not set, default to current directory
if [ -z $POLYPHONIC_OMR ]; then
    POLYPHONIC_OMR="./"
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

in_dir=$(get_arg $1 '2_musicxml_parts')
out_dir=$(get_arg $2 '5_labels_semantic')

echo ""
echo "================================================"
echo "Running 100/run_2_to_5.sh"
echo "musicxml parts -> semantic labels using polyphonic OMR/label_gen/genlabels.py"
echo "================================================"
echo ""


# ================================ MAIN ================================

mkdir -p $out_dir

# Split parts
python $POLYPHONIC_OMR/label_gen/genlabels.py \
    --input-folder $in_dir \
    --output-folder $out_dir
