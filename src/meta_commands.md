# Meta commands

## Links

[Begginers guide](https://wiki.metacentrum.cz/wiki/Beginners_guide)
[Pruvodce pro začátečníky](https://wiki.metacentrum.cz/wiki/Pruvodce_pro_zacatecniky)

### metacentrum FE login
ssh xvlach22@skirit.ics.muni.cz s heslem Vojtus1…_

### Metacentrum BE login **for scratch dir after exit**
ssh xvlach22@black1.cerit-sc.cz

### Copy updated pero to metacentrum:
scp -r ~/skola/BP/code_from_others xvlach22@storage-brno2.metacentrum.cz:~/bp_omr/

### Copy experiments to local
scp -r xvlach22@storage-brno2.metacentrum.cz:~/bp_omr/experiments ~/skola/BP/experiments


## Start job
např. 
qsub -I -l select=1:ncpus=2:mem=10gb:scratch_local=10gb -l walltime=00:30:00
qsub -I -l select=1:ncpus=2:mem=20gb:scratch_local=20gb -l walltime=00:30:00
### with GPU
qsub -I -l select=1:ncpus=2:ngpus=1:mem=25gb:scratch_local=25gb -q gpu -l walltime=0:30:0

### with GPU+SSD
qsub -I -l select=1:ncpus=2:ngpus=1:mem=30gb:scratch_ssd=30gb -q gpu -l walltime=1:0:0
qsub -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_ssd=20gb:gpu_cap=cuda60 -q gpu -l walltime=0:30:0
### with GPU+SSD+BLACK cluster
qsub -I -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_ssd=20gb:cluster=black -q gpu -l walltime=0:30:0
### with GPU+SSD+Grimbold cluster
qsub -I -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_local=20gb:cluster=grimbold -q gpu -l walltime=1:0:0

### job setter
export EXPERIMENT="230109_first_try" && cd $SCRATCH && cp -r /storage/brno2/home/xvlach22/bp_omr/* $SCRATCH && cd experiments/$EXPERIMENT && chmod u+x run_experiment.sh && trap 'cp -r $SCRATCH/experiments /storage/brno2/home/xvlach22/bp_omr/experiments/scratch_copy ; clean_scratch' EXIT TERM && module add python36-modules-gcc
**OR**
cp /storage/brno2/home/xvlach22/bp_omr/experiments/230111_there_is_no_more_try_just_do/run_experiment.sh run_experiment.sh && chmod u+x run_experiment.sh

**+**
./run_experiment.sh

### Copy from job to storage
cp -r . /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT

### clean_scratch
clean_scratch 
    or trap 'clean_scratch' TERM EXIT



## Other commands

pip3.6 index versions shapely
torch>=1.10.2 NEBO 1.8.0 aaa



## How server work CuDNN or not
black1  OK
grimbold OK

adan1-61 NOP
gita1-7 NOP
zia3    NOP
