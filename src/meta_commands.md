# Meta commands

pip3.6 index versions shapely
torch>=1.10.2 NEBO 1.8.0 aaa


## Start job
např. 
qsub -I -l select=1:ncpus=2:mem=10gb:scratch_local=10gb -l walltime=00:30:00
qsub -I -l select=1:ncpus=2:mem=20gb:scratch_local=20gb -l walltime=00:30:00
### with GPU
qsub -I -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_local=20gb -q gpu -l qalltime=0:30:0

export EXPERIMENT="230106_first_try" && cd $SCRATCH && cp -r /storage/brno2/home/xvlach22/bp_omr/* $SCRATCH && cd experiments/$EXPERIMENT && chmod u+x run_experiment.sh && trap 'cp -r $SCRATCH/experiments /storage/brno2/home/xvlach22/bp_omr/experiments/scratch_copy ; clean_scratch' EXIT TERM && module add python36-modules-gcc

./run_experiment.sh


cp -r . /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT


clean_scratch 
    or trap 'clean_scratch' TERM EXIT

