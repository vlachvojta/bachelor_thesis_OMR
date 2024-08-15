#!/bin/bash

# get location of this script
LOCAL=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

get_arg() {
    if [ -z "$1" ]; then
        echo $2 # return default value
    else
        echo $1 # return argument value
    fi
}

data_dir=$(get_arg $1 './')
sub_dir=$(get_arg $2 '')


time_start=$(date +%s)

# ./run_0_to_1_musescore3.sh 0_orig_mscz/$sub_folder 1_musicxml_by_M3_CLI/$sub_folder  && \
# ./run_1_to_2.sh 1_musicxml_by_M3_CLI/$sub_folder 2_musicxml_parts/$sub_folder  && \
$LOCAL/run_0_to_1_musescore4.sh $data_dir/0_orig_mscz/$sub_dir $data_dir/1_musicxml_by_M4_CLI/$sub_dir  && \
$LOCAL/run_1_to_2.sh $data_dir/1_musicxml_by_M4_CLI/$sub_dir $data_dir/2_musicxml_parts/$sub_dir  && \
$LOCAL/run_2_to_3_musescore4.sh $data_dir/2_musicxml_parts/$sub_dir $data_dir/3_img_pages/$sub_dir  && \
# ./run_2_to_3_musescore3.sh 2_musicxml_parts/$sub_folder 3_img_pages/$sub_folder  && \ 
$LOCAL/run_3_to_4.sh $data_dir/3_img_pages/$sub_dir $data_dir/4_img_staves/$sub_dir  && \
$LOCAL/run_2_to_5.sh $data_dir/2_musicxml_parts/$sub_dir $data_dir/5_labels_semantic/$sub_dir  && \
$LOCAL/run_5_to_6.sh $data_dir/4_img_staves/$sub_dir $data_dir/5_labels_semantic/$sub_dir $data_dir/6_copied_pairs/$sub_dir  && \
# ./run_6_to_7.sh

echo ""
echo "Pipeline 100 complete"
time_end=$(date +%s)
time_diff=$((time_end - time_start))
echo "Time taken by running pipeline 100: $time_diff seconds"
