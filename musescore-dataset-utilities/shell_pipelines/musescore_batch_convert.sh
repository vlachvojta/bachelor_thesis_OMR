#!/bin/bash

# Bash script for automatic converting files using MuseScore Command line interface
# Author: Vojtěch Vlach
# Contact: xvlach22@vutbr.cz
# Usage: ./musescore_batch_convert.sh <input_extension> <output_extension> <input_directory> <output_directory> [<musescore_version>]


# ================================ PARAMETERS ================================
# Return default value if argument is empty
get_arg() {
    if [ -z "$1" ]; then
        echo $2 # return default value
    else
        echo $1 # return argument value
    fi
}

# input files extension
in_ext=$(get_arg $1 'mscz')
out_ext=$(get_arg $2 'musicxml')
in_dir=$(get_arg $3 '.')
out_dir=$(get_arg $4 './output_musescore_batch_convert')
musescore_version=$(get_arg $5 'musescore3')

if [ ! -d "$in_dir" ]; then
    echo "Input directory $in_dir does not exist"
    exit 1
fi

# check $musescore_version is either musescore4portable or musescore3
if [ "$musescore_version" != "musescore3" ] && [ "$musescore_version" != "musescore4portable" ]; then
    echo "Invalid MuseScore version. Use musescore3 or musescore4portable"
    exit 1
fi

# echo "musescore $in_dir/*.$in_ext -o $out_dir/*.$out_ext"
echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext"

# ================================ MAIN ================================

# find all files with input extension in the directory
ls $in_dir/*.$in_ext | while read file; do
    file=$(basename $file) # remove path
    file=$(echo "${file%.$in_ext}") # remove file suffix

    # echo "Converting $file.$in_ext to $file.$out_ext"
    # echo "Checking if ${out_dir}/${file}*.${out_ext} exists"

    # check if the output file already exists
    if [ ! "$(ls ${out_dir}/${file}*.${out_ext} 2>/dev/null)" ]; then
        echo "$file.$in_ext"  # print the name of the file (-e for escape sequences, -n for no newline)
        # musescore3 $in_dir/$file -o ${out_dir}/${file%}.$out_ext  2> /dev/null
        #musescore3 $in_dir/$file.$in_ext -o $out_dir/$file.$out_ext  2> /dev/null
        $musescore_version $in_dir/$file.$in_ext -o $out_dir/$file.$out_ext  2> /dev/null
    else
        echo -n "."
    fi
done
# sort -r to process files in reverse order for some reason

echo ""
echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext finished"

