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

in_progress_dir=$in_dir/in_progress
if [ ! -d "$in_progress_dir" ]; then
    mkdir -p $in_progress_dir
fi

done_dir=$in_dir/done
if [ ! -d "$done_dir" ]; then
    mkdir -p $done_dir
fi

echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext"

# ================================ MAIN ================================

files_done=$(ls $done_dir/*.$in_ext 2>/dev/null | wc -l)
num_files=$(ls $in_dir/*.$in_ext | wc -l)
num_files=$((num_files + files_done))
i=$files_done

# find all files with input extension in the directory
ls $in_dir/*.$in_ext | while read file; do
    file=$(basename $file) # remove path
    file=$(echo "${file%.$in_ext}") # remove file suffix

    # check if the output file already exists
    if [ ! "$(ls ${out_dir}/${file}*.${out_ext} 2>/dev/null)" ]; then
        echo -e "$file.$in_ext \t $i/$num_files \t $(date "+%Y%m%d-%H%M%S")"

        # move file to in_progress directory to parse it there
        mv $in_dir/$file.$in_ext $in_progress_dir

        # Add this grep if you want to filter out some warnings from stderr
        # 2>&1 | grep -v "/lib/x86_64-linux-gnu/lib"
        $musescore_version -f $in_progress_dir/$file.$in_ext -o $out_dir/$file.$out_ext 2>/dev/null

        # save exit code
        mscz_exit_code=$?
        echo "Exit code: $mscz_exit_code"

        # if exit code is not 0, move file to error directory
        if [ $mscz_exit_code -ne 0 ]; then
            mkdir -p $in_dir/err_$mscz_exit_code
            mv $in_progress_dir/$file.$in_ext $in_dir/err_$mscz_exit_code
        else
            # move file to done directory
            mv $in_progress_dir/$file.$in_ext $done_dir
        fi

    else
        # move file to done directory
        mv $in_dir/$file.$in_ext $done_dir
        echo -n "."
    fi
    i=$((i+1))
done
# sort -r to process files in reverse order for some reason

echo ""
echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext finished"

