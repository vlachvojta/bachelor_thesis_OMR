#!/usr/bin/env bash
#PBS -l select=1:ncpus=2:ngpus=1:mem=15gb:scratch_local=10gb:cluster=black
#PBS -q gpu@cerit-pbs.cerit-sc.cz
#PBS -N TODO_EXPERIMENT_NAME_1/2
#PBS -l walltime=6:0:0
#PBS -m abe

EXPERIMENT="TODO_EXPERIMENT_NAME_2/2"
cd $SCRATCH
echo "SCRATCH: "$SCRATCH
cp -r /storage/brno2/home/xvlach22/bp_omr/datasets $SCRATCH/datasets
mkdir $SCRATCH/experiments
cp -r /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT $SCRATCH/experiments/$EXPERIMENT
cp -r /storage/brno2/home/xvlach22/bp_omr/ubuntu_fonts $SCRATCH/ubuntu_fonts
cp -r /storage/brno2/home/xvlach22/bp_omr/code_from_others $SCRATCH/code_from_others
cd experiments/$EXPERIMENT
mkdir tmp
# chmod u+x run_experiment.sh

trap 'cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/ ; echo "data saved back to storage" ; clean_scratch' EXIT TERM

module add python36-modules-gcc
pip3.6 install --upgrade pip 1>/dev/null

HOME=$SCRATCH
PERO_PATH=$HOME"/code_from_others/pero"
PERO_OCR_PATH=$HOME"/code_from_others/pero-ocr"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH
export PATH=$PATH:$PYTHONPATH

# Dataset
LMDB=$HOME"/datasets/images.lmdb"
DATA_TST=$HOME"/datasets/data_2.tst" # data_2.tst: SAgnostic, data.tst: SSemantic

# Python scripts
EXPORT_PY=$PERO_PATH"/pytorch_ctc/export_model.py"
GET_LOGITS_PY=$PERO_PATH"/karelb-ocr-scripts/get_folder_logits.py"
DECODE_PY=$PERO_PATH"/karelb-ocr-scripts/decode_logits.py"

# Python script arguments
NET=VGG_LSTM_B64_L17_S4_CB4
CHECKPOINT_PATH=$HOME"/experiments/"$EXPERIMENT"/checkpoints/"
TMP=$HOME"/experiments/"$EXPERIMENT"/tmp/"
OCR_JSON=$TMP"/out.json"
OCR_MODEL=$TMP"/out.pt"
PICKLE=$TMP"/pickle_out.pkl"
CONFIDENCE=$TMP"/confidence.del"

echo "ls $CHECKPOINT_PATH/checkpoint_*.pth" | tee -a log_x.txt
ls $CHECKPOINT_PATH/checkpoint_*.pth | tee -a log_x.txt

pip3.6 install safe_gpu lmdb opencv-python scipy brnolm 1>/dev/null
pip3.6 install torchvision==0.2.2 1>/dev/null

for checkpoint in `ls -r $CHECKPOINT_PATH/checkpoint_*.pth`; do
    SECONDS=0  # start meassuring time
    echo ""
    echo "=================================== $checkpoint"
    if [ -f $checkpoint.out ]; then
        echo "File $checkpoint.out already exists"
    else
        echo "----runnning export_model.py----"
        python3.6 -u $EXPORT_PY  \
            --path $checkpoint --net $NET  \
            --line-height 100 --line-vertical-scale 2705  \
            --output-json-path $OCR_JSON \
            --output-model-path $OCR_MODEL  \
            --trace

        echo "----runnning get_folder_logits.py----"
        python3.6 -u $GET_LOGITS_PY  \
            --ocr-json $OCR_JSON --input $LMDB  \
            --lines $DATA_TST --output $PICKLE

        echo "----runnning decode_logits.py----"
        python3.6 -u $DECODE_PY \
            --ocr-json $OCR_JSON \
            --input $PICKLE \
            --best $checkpoint".out" --greedy \
            --confidence $CONFIDENCE

        cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/
        echo ""
        echo "data saved back to a data server"
        echo "This checkpoint took: $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
    fi
done 2>&1 | tee -a log_x.txt

cp -r $SCRATCH/experiments/$EXPERIMENT /storage/brno2/home/xvlach22/bp_omr/experiments/
clean_scratch
exit
