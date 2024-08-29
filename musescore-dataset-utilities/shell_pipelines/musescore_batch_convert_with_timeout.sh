#!/bin/bash

# Bash script for automatic converting files using MuseScore Command line interface
# Author: Vojtěch Vlach
# Contact: xvlach22@vutbr.cz
# Usage: ./musescore_batch_convert.sh <input_extension> <output_extension> <input_directory> <output_directory> [<musescore_version>] [<timeout>]


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
timeout=$(get_arg $6 15)

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

num_files=$(ls $in_dir/*.$in_ext | wc -l)
i=0

# find all files with input extension in the directory
ls $in_dir/*.$in_ext | while read file; do
    file=$(basename $file) # remove path
    file=$(echo "${file%.$in_ext}") # remove file suffix

    # echo "Converting $file.$in_ext to $file.$out_ext"
    # echo "Checking if ${out_dir}/${file}*.${out_ext} exists"

    # check if the output file already exists
    if [ "$(ls ${out_dir}/${file}*.${out_ext} 2>/dev/null)" ]; then
        echo -n "." # file exists
    else
        echo ""
        echo -e "$file.$in_ext \t $i/$num_files"

        musescore_command=("$musescore_version" "$in_dir/$file.$in_ext" "-o" "$out_dir/$file.$out_ext")
        "${musescore_command[@] 2>/dev/null}" &
        runnerpid=$!
        echo "runnerpid: $runnerpid"
        echo "Started MuseScore with PID: $runnerpid"

        # Immediately check the process
        echo "Immediate ps -p $runnerpid:"
        ps -p $runnerpid

        # first option:
        # start checking periodically if the musesore background process stil runs
        end_time=$((SECONDS + timeout))
        while [ $SECONDS -lt $end_time ]; do
            if ! ps -p $runnerpid > /dev/null; then
                echo "Exiting the loop if the process is no longer running"
                break # Exit the loop if the process is no longer running
            fi
            echo "sleeping 1 second"
            sleep 1 # Short sleep to avoid consuming too much CPU
        done

        # At this point, the MuseScore process has either finished or timed out
        if ps -p $runnerpid > /dev/null; then
            echo "Command timed out."
            kill -SIGKILL $runnerpid 2>/dev/null
            # Perform any additional actions here
        fi

        # second option:
        start_time=$SECONDS
        while true; do
            if ! kill -0 $runnerpid 2>/dev/null; then
                echo "MuseScore process finished."
                break
            fi
            current_time=$SECONDS
            elapsed_time=$((current_time - start_time))
            if [ $elapsed_time -ge $timeout ]; then
                echo "Command timed out."
                kill -SIGKILL $runnerpid 2>/dev/null
                break
            fi
            sleep 1
        done


    fi
    i=$((i+1))
done
# sort -r to process files in reverse order for some reason

echo ""
echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext finished"

