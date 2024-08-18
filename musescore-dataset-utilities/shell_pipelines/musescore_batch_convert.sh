#!/bin/bash

# Bash script for automatic converting files using MuseScore Command line interface
# Author: Vojtěch Vlach
# Contact: xvlach22@vutbr.cz
# Usage: ./musescore_batch_convert.sh <input_extension> <output_extension> <input_directory> <output_directory> [<musescore_version>]

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

# input files extension
in_ext=$(get_arg $1 'mscz')
out_ext=$(get_arg $2 'musicxml')
in_dir=$(get_arg $3 '.')
out_dir=$(get_arg $4 './output_musescore_batch_convert')
musescore_version=$(get_arg $5 'musescore4portable') # options: musescore3, musescore4portable
style_arg=$(get_arg $6 'default') # options: default, random, muse_jazz, bold, nsm, colornotes, notenames

if [ ! -d "$in_dir" ]; then
    echo "Input directory $in_dir does not exist"
    exit 1
fi

if [ ! -d "$out_dir" ]; then
    mkdir -p $out_dir
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

styles_dir=$BP_GIT/musescore-dataset-utilities/mscz_styles

echo "$musescore_version $in_dir/*.$in_ext -o $out_dir/*.$out_ext"

# ================================ FUNCTIONS FOR CONVERTING ================================

convert_with_musescore() {
    # $1 musecore version, $2 input file, $3 output file
    musescore_version=$1
    input_file=$2
    output_file=$3
    style=$4

    if [ "$style" == "default" ]; then
        echo "Style: default"
        convert_with_musescore_default $musescore_version $input_file $output_file
    elif [ "$style" == "muse_jazz" ]; then
        echo "Style: muse_jazz"
        convert_with_musescore_muse_jazz $musescore_version $input_file $output_file
    elif [ "$style" == "bold" ]; then
        echo "Style: bold"
        convert_with_musescore_bold $musescore_version $input_file $output_file
    elif [ "$style" == "nsm" ]; then
        echo "Style: nsm"
        convert_with_musescore_nsm $musescore_version $input_file $output_file
    elif [ "$style" == "colornotes" ]; then
        echo "Style: colornotes"
        convert_with_musescore_colornotes $musescore_version $input_file $output_file
    elif [ "$style" == "notenames" ]; then
        echo "Style: notenames"
        convert_with_musescore_notenames $musescore_version $input_file $output_file
    elif [ "$style" == "random" ]; then
        styles=("default" "default" "default" "default" \
            "nsm" "nsm" \
            "muse_jazz" "muse_jazz"  \
            "bold" "bold"  \
            "colornotes" "notenames")
        random_style=${styles[$RANDOM % ${#styles[@]}]}
        convert_with_musescore $musescore_version $input_file $output_file $random_style
    else
        echo "Invalid style. Use default, muse_jazz, bold, nsm, colornotes, notenames or random"
    fi

    return $?

    # convert_with_musescore_default $musescore_version $input_file $output_file
    # convert_with_musescore_muse_jazz $musescore_version $input_file $output_file
    # convert_with_musescore_bold $musescore_version $input_file $output_file
    # convert_with_musescore_nsm $musescore_version $input_file $output_file
    # convert_with_musescore_colornotes $musescore_version $input_file $output_file
    # convert_with_musescore_notenames $musescore_version $input_file $output_file
}

convert_with_musescore_default() {
    # $1 musecore version, $2 input file, $3 output file
    musescore_version=$1
    input_file=$2
    output_file=$3

    $musescore_version $input_file -o $output_file -f 2>/dev/null
    return $?
}

convert_with_musescore_muse_jazz() {
    # $1 musecore version, $2 input file, $3 output file
    $1 -f -S $styles_dir/muse_jazz.mss $2 -o $3 2>/dev/null
    return $?
}

convert_with_musescore_bold() {
    # $1 musecore version, $2 input file, $3 output file
    $1 -f -S $styles_dir/bold.mss $2 -o $3 2>/dev/null
    return $?
}

convert_with_musescore_nsm() {
    # $1 musecore version, $2 input file, $3 output file
    $1 -f -S $styles_dir/nsm.mss $2 -o $3 2>/dev/null
    return $?
}

convert_with_musescore_colornotes() {
    # $1 musecore version, $2 input file, $3 output file
    create_job_json $2 $3 "colornotes.qml" | jq . > $in_dir/colornotes_job.json

    musescore3 -f -j $in_dir/colornotes_job.json 2>/dev/null
    # musescore4 does not support -j option apparently
    return $?
}

convert_with_musescore_notenames() {
    # $1 musecore version, $2 input file, $3 output file
    create_job_json $2 $3 "notenames.qml" | jq . > $in_dir/notenames_job.json

    musescore3 -f -j $in_dir/notenames_job.json 2>/dev/null
    # musescore4 does not support -j option apparently
    return $?
}

create_job_json() {
    # $1 input file, $2 output file, $3 plugin
    echo '[{"in": "'$1'", "out": "'$2'", "plugin": "'$3'" } ]'
}


# ================================ MAIN ================================

# count files in directories to show progress n/N
files_done=$(ls $done_dir/*.$in_ext 2>/dev/null | wc -l)
files_err=$(ls $in_dir/err_*/*.$in_ext 2>/dev/null | wc -l)
files_in_progress=$(ls $in_progress_dir/*.$in_ext 2>/dev/null | wc -l)
num_files=$(ls $in_dir/*.$in_ext | wc -l)
num_files=$((num_files + files_done + files_err + files_in_progress))
i=$((files_done + files_err + files_in_progress))

# find all files with input extension in the directory
ls $in_dir/*.$in_ext | while read file; do
    file=$(basename $file) # remove path
    file=$(echo "${file%.$in_ext}") # remove file suffix

    # check if the output file already exists
    if [ ! "$(ls ${out_dir}/${file}*.${out_ext} 2>/dev/null)" ]; then
        echo -e "$file.$in_ext \t $i/$num_files \t $(date "+%Y%m%d-%H%M%S")"

        # move file to in_progress directory to parse it there
        mv $in_dir/$file.$in_ext $in_progress_dir

        convert_with_musescore $musescore_version $in_progress_dir/$file.$in_ext $out_dir/$file.$out_ext $style_arg
        # Add this grep if you want to filter out some warnings from stderr
        # 2>&1 | grep -v "/lib/x86_64-linux-gnu/lib"

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

