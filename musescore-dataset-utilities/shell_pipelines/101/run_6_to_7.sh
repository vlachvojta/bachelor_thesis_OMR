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
out_yolo_dir=$(get_arg $2 '7_yolo_detected')


echo ""
echo "================================================"
echo "Running 100/run_6_to_7.sh"
echo "Resizing images to 1024x1458, detecting staves with YOLO, runnning mathcmaker"
echo "================================================"
echo ""


# ================================ MAIN ================================

mkdir -p $out_dir

# for every file in in_dir, resize to 1024x1458, save to the same file in in_dir (overwrite)
for file in $(ls -1q $in_dir/*.png); do
    echo "Resizing $file"
    convert $file \
        -resize 1024x1458 \
        -background white \
        -gravity center \
        -extent 1024x1458 $file
done

# for every file in in_dir, run YOLOv5 to detect staves, 
# save stave cut-outs but only if there is one staff detected
python $BP_GIT/musescore-dataset-utilities/yolo_detect.py \
    --model /mnt/matylda1/ikiss/orbis/experiments/yolov8/2024-08-15_training/yolov8s_1024px_extra-music/orbis/yolov8s_1024px_extra-music/weights/best.pt \
    --images $in_dir \
    --crops $out_dir/crops \
    --image-size 1024 \
    --confidence 0.283 \
    --batch-size 1 \
    --renders $out_dir/renders

