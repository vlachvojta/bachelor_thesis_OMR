#!/bin/bash

# description: Convert mscz to musicxml using Musescore CLI
# parameters: input folder, output folder

# get location of this script
LOCAL=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# ================================ PARAMETERS ================================
# Return default value if argument is empty
get_arg() {
    if [ -z "$1" ]; then
        echo $2 # return default value
    else
        echo $1 # return argument value
    fi
}

in_dir=$(get_arg $1 '0_orig_mscz')
out_dir=$(get_arg $2 '1_musicxml_by_M3_CLI')

echo ""
echo "================================================"
echo "Running 100/run_0_to_1_musescore3.sh"
echo "mscz -> musicxml using Musescore 3 CLI"
echo "================================================"
echo ""

# ================================ MAIN ================================

mkdir -p $out_dir
$LOCAL/../musescore_batch_convert.sh mscz musicxml $in_dir $out_dir musescore3
