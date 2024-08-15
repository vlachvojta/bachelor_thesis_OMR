#!/bin/bash

# description: Convert musicxml parts to png images
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

in_dir=$(get_arg $1 '2_musicxml_parts')
out_dir=$(get_arg $2 '3_img_pages')

echo ""
echo "================================================"
echo "Running 100/run_2_to_3_musescore4.sh"
echo "musicxml parts -> png images using Musescore 4 CLI"
echo "================================================"
echo ""

# ================================ MAIN ================================

mkdir -p $out_dir
$LOCAL/../musescore_batch_convert.sh musicxml png $in_dir $out_dir musescore4portable
