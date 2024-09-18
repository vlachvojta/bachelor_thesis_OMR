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

in_dir=$(get_arg $1 '6_copied_pairs')
out_dir=$(get_arg $2 '7_yolo_detected')


echo ""
echo "================================================"
echo "Running 100/run_6_to_7.sh"
echo "Resizing images to 1024x1458, detecting staves with YOLO, copying only corresponding labels"
echo "in_dir: $in_dir, out_dir: $out_dir"
echo "================================================"
echo ""


# ================================ MAIN ================================

files=$(ls -1q $in_dir/*.png | wc -l)
echo "Number of images in $in_dir: $files"

i=0

# for every file in in_dir, resize to 1024x1458, save to the same file in in_dir (overwrite)
for file in $(ls -1q $in_dir/*.png); do
    if [ $((i % 1000)) -eq 0 ]; then
        echo "Resizing image $i"
    fi
    convert $file \
        -resize 1024x1458 \
        -background white \
        -gravity North \
        -extent 1024x1458 $file
    i=$((i+1))
done

mkdir -p $out_dir

# for every file in in_dir, run YOLOv5 to detect staves, 
# save stave cut-outs but only if there is one staff detected
python $BP_GIT/musescore-dataset-utilities/yolo_detect.py \
    --model /mnt/matylda1/ikiss/orbis/experiments/yolov8/2024-08-15_training/yolov8s_1024px_extra-music/orbis/yolov8s_1024px_extra-music/weights/best.pt \
    --images $in_dir \
    --crops $out_dir \
    --labels $out_dir/yolo_labels \
    --image-size 1024 \
    --confidence 0.283 \
    --batch-size 20 \
    # --renders $out_dir/yolo_renders

# for every image in $out_dir, copy the corresponding label from $in_dir/0_labels.SSemantic
# to $out_dir/0_labels.SSemantic

# print how many images are in $out_dir
files=$(ls -1q $out_dir/*.png | wc -l)
echo "Number of images in $out_dir: $files"
echo "Copying corresponding labels from $in_dir/0_labels.SSemantic to $out_dir/0_labels.SSemantic"

rm -f $out_dir/0_labels.SSemantic
touch $out_dir/0_labels.SSemantic

# copy labels only for correctly cut-out images (for every png file in $out_dir, copy the corresponding label from $in_dir/0_labels.SSemantic)
for file in $(ls -1q $out_dir/*.png); do
    filename=$(basename $file)
    grep $filename $in_dir/0_labels.SSemantic >> $out_dir/0_labels.SSemantic
done
