#!/bin/sh
### General options
### –- specify queue --
# BSUB -q gpua100
### -- set the job Name --
# BSUB -J monodetr1_
### -- ask for number of cores (default: 1) --
# BSUB -n 4
### -- Select the resources: 1 gpu in exclusive process mode --
# BSUB -gpu "num=1:mode=exclusive_process"
### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
# BSUB -W 1:00
# request 5GB of system-memory
# BSUB -R "rusage[mem=5GB]"
### -- set the email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
# BSUB -u s222999@dtu.dk
### -- send notification at start --
# BSUB -B
### -- send notification at completion--
# BSUB -N
### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
# BSUB -o monodetr1_%J.out
# BSUB -e monodetr1_%J.err
# -- end of LSF options --

# -- load modules -- 
module load cuda/11.1
module load gcc/7.5.0
module list
# -- end of load modules -- 

conda activate monodetr
echo "Conda env activated"

/work3/s222999/miniconda3/envs/monodetr/bin/python tools/train_val.py --config $@

echo "It run correctly!"