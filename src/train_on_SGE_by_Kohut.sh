#$ -l h='!(pcgpu4|supergpu14)' ram_free=26G,gpu=1,gpu_ram=20G,tmp_free=25G
#$ -N D_32
#$ -o /mnt/matylda1/ikohut/SGE_test/out.out
#$ -e /mnt/matylda1/ikohut/SGE_test/err.err
#$ -q long.q@@gpu

source /mnt/matylda1/ikohut/environments/pytorch_1.10/bin/activate
PERO_PATH="/mnt/matylda1/ikohut/pero.master.2022-04-08/"
PERO_OCR_PATH="/mnt/matylda1/ikohut/pero-ocr/"
export PYTHONPATH=$PERO_PATH:$PERO_OCR_PATH

DATE="2022-04-08"
NET_NAME="LSTM_BC_3_BLC_2_BFC_64_FRN"

BASE_FOLDER="/mnt/matylda1/hradis/PERO/datasets_lmdb/HWR.2022-04-06/"

TRN_DATA=$BASE_FOLDER"dataset_gt/out.final/data.trn"
TST_DATA=$BASE_FOLDER"dataset_gt/out.final/data.tst"


LMDB_PATH_HOST=$BASE_FOLDER"lmdb.hwr_40-1.0"

FONT="/mnt/matylda1/ikohut/fonts/Ubuntu-R.ttf"

DATA_MANIPULATOR="UNIVERSAL_HWR"
MAX_LINE_WIDTH=1512
MAX_BUFFER_SIZE=20000000000
MAX_BUFFERED_LINES=1000000

CHARS_SET_NAME="all"

OPTIMIZER="Adam"
LEARNING_RATE=0.0003
BATCH_SIZE=32
DROPOUT_RATE=0.1
START_ITER=0
MAX_ITERATIONS=200000

WARM_UP_ITERATIONS=10000
WARM_UP_POLYNOMIAL_ORDER=3

TEST_STEP=1000
SAVE_STEP=10000

EXPERIMENT_DIR="/mnt/matylda1/ikohut/experiments/pero-ocr.fit.vutbr.cz_HWR.2022-04-06/training/"$NET_NAME"."$DATE"/"
mkdir -p $EXPERIMENT_DIR
CHECKPOINT_DIR=$EXPERIMENT_DIR"checkpoints"
mkdir -p $CHECKPOINT_DIR
SHOW_DIR=$EXPERIMENT_DIR"show"
mkdir -p $SHOW_DIR

LOG=$EXPERIMENT_DIR$NET_NAME"."$DATE"_"$START_ITER".log"

mkdir /tmp/ikohut
LMDB_PATH_DEVICE="/tmp/ikohut/lmdb_"$NET_NAME"."$DATE"_"$START_ITER
cp -r $LMDB_PATH_HOST $LMDB_PATH_DEVICE

sync


python3 -u $PERO_PATH"pytorch_ctc/train_pytorch_ocr.py" \
		     --net $NET_NAME \
                     --trn-data $TRN_DATA \
                     --tst-data $TST_DATA \
		     --lmdb-path $LMDB_PATH_DEVICE \
                     --data-manipulator $DATA_MANIPULATOR \
                     --max-line-width $MAX_LINE_WIDTH \
                     --max-buffer-size $MAX_BUFFER_SIZE \
		     --max-buffered-lines $MAX_BUFFERED_LINES \
		     --chars-set $CHARS_SET_NAME \
                     --normalization-scale-std $NORMALIZATION_SCALE_STD \
                     --optimizer $OPTIMIZER \
                     --learning-rate $LEARNING_RATE \
                     --batch-size $BATCH_SIZE \
		     --dropout-rate $DROPOUT_RATE \
		     --start-iteration $START_ITER \
		     --max-iterations $MAX_ITERATIONS \
                     --warm-up-iterations $WARM_UP_ITERATIONS \
                     --warm-up-polynomial-order $WARM_UP_POLYNOMIAL_ORDER \
		     --test-step $TEST_STEP \
                     --save-step $SAVE_STEP \
		     --checkpoint-dir $CHECKPOINT_DIR \
                     --show-trans \
		     --test \
		     --show-dir $SHOW_DIR \
		     --sample-similar-length \
		     --font $FONT > $LOG 2>&1

rm -r $LMDB_PATH_DEVICE

echo DONE
