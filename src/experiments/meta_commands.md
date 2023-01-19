# Meta commands
- [Meta commands](#meta-commands)
  - [Links](#links)
  - [Commands](#commands)
    - [Start job](#start-job)
    - [job setter](#job-setter)
    - [Copy from job to storage](#copy-from-job-to-storage)
    - [clean\_scratch](#clean_scratch)
    - [Other commands](#other-commands)
  - [Which clusters work CuDNN error and which don't](#which-clusters-work-cudnn-error-and-which-dont)

## Links
- [Begginers guide](https://wiki.metacentrum.cz/wiki/Beginners_guide)
- [Pruvodce pro začátečníky](https://wiki.metacentrum.cz/wiki/Pruvodce_pro_zacatecniky)
- [Frontendy](https://wiki.metacentrum.cz/wiki/Frontend)
- [GPU clusters](https://wiki.metacentrum.cz/wiki/GPU_clusters)
- [About scheduling system](https://wiki.metacentrum.cz/wiki/About_scheduling_system)
- [get-job-history](https://wiki.metacentrum.cz/wiki/PBS_get_job_history)
- [Command builder qsub](https://metavo.metacentrum.cz/pbsmon2/qsub_pbspro)
- [Python modules](https://metavo.metacentrum.cz/pbsmon2/qsub_pbspro)
- [Working with data](https://wiki.metacentrum.cz/wiki/Working_with_data)
- [How NOT to take down metacentre](https://www.cesnet.cz/wp-content/uploads/2021/04/Vorel_MC_2021.pdf)

## Commands
- metacentrum FE login
  - ssh xvlach22@skirit.ics.muni.cz s heslem Vojtus1…_

- Metacentrum BE login **for scratch dir after exit**
  - ssh xvlach22@black1.cerit-sc.cz

- Copy updated pero to metacentrum:
  - scp -r ~/skola/BP/code_from_others xvlach22@storage-brno2.metacentrum.cz:~/bp_omr/

- Copy experiments to local
  - scp -r xvlach22@storage-brno2.metacentrum.cz:~/bp_omr/experiments ~/skola/BP/experiments

### Start job
- např. 
  - qsub -I -l select=1:ncpus=2:mem=10gb:scratch_local=10gb -l walltime=00:30:00
  - qsub -I -l select=1:ncpus=2:mem=20gb:scratch_local=20gb -l walltime=00:30:00
- with GPU
  - qsub -I -l select=1:ncpus=2:ngpus=1:mem=25gb:scratch_local=25gb -q gpu -l walltime=0:30:0

- with GPU+SSD
  - qsub -I -l select=1:ncpus=2:ngpus=1:mem=30gb:scratch_ssd=30gb -q gpu -l walltime=1:0:0
  - qsub -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_ssd=20gb:gpu_cap=cuda60 -q gpu -l walltime=0:30:0
- with GPU+SSD+BLACK cluster
  - qsub -I -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_ssd=20gb:cluster=black -q gpu -l walltime=0:30:0
  - OR nonInteractive
  - qsub -l walltime=2:0:0 -q gpu@cerit-pbs.cerit-sc.cz -l select=1:ncpus=2:ngpus=1:mem=12gb:scratch_ssd=10gb:cluster=black run_experiment_auto.sh
- with GPU+SSD+Grimbold cluster
  - qsub -I -l select=1:ncpus=2:ngpus=1:mem=20gb:scratch_local=20gb:cluster=grimbold -q gpu -l walltime=1:0:0
- with GPU+KONS cluster
  - qsub -I -l walltime=2:0:0 -q gpu -l select=1:ncpus=2:ngpus=1:mem=12gb:scratch_local=10gb:cluster=konos
  - OR nonInteractive:
  - qsub -l walltime=2:0:0 -q gpu -l select=1:ncpus=2:ngpus=1:mem=12gb:scratch_local=10gb:cluster=konos run_experiment_auto.sh
  - \+ kontrola průběhu pomocí: ssh konos3.fav.zcu.cz

### job setter
- export EXPERIMENT="230109_first_try" && cd \$SCRATCH && cp -r /storage/brno2/home/xvlach22/bp_omr/\* \$SCRATCH && cd experiments/$EXPERIMENT && chmod u+x run_experiment.sh && trap 'cp -r $SCRATCH/experiments /storage/brno2/home/xvlach22/bp_omr/experiments/scratch_copy ; clean_scratch' EXIT TERM && module add python36-modules-gcc
- **OR the semi auto:**
- cp /storage/brno2/home/xvlach22/bp_omr/experiments/230112_safe_gpu_semi_auto/run_experiment.sh run_experiment.sh && chmod u+x run_experiment.sh
- **+**
- ./run_experiment.sh

### Copy from job to storage
- cp -r . /storage/brno2/home/xvlach22/bp_omr/experiments/$EXPERIMENT

### clean_scratch
- clean_scratch 
- or trap 'clean_scratch' TERM EXIT

### Other commands

- pip3.6 index versions shapely
  - show possible versions for python module


## Which clusters work CuDNN error and which don't
OK:
- konos1-8    fav.zcu ??? (can schedule through meta-pbs.metacentrum.cz)
- black1      cerit
- grimbold    meta
- (glados10-13 OK)

NOP:
- glados1-7   NOP
- galdor1-20  NOP
- adan1-61    NOP
- fau1-3      NOP
- gita1-7     NOP
- luna        NOP
- zia3        NOP
