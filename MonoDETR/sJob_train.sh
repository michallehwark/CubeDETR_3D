#!/bin/sh
### General options
### –- specify queue --
#BSUB -q gpuv100
### -- set the job Name --
#BSUB -J monodetr4_
### -- ask for number of cores (default: 1) --
#BSUB -n 4
### -- Select the resources: 1 gpu in exclusive process mode --
#BSUB -gpu "num=1:mode=exclusive_process"
### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
#BSUB -W 1:00
# request 5GB of system-memory
#BSUB -R "rusage[mem=5GB]"
### -- set the email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
# BSUB -u s222999@dtu.dk
### -- send notification at start --
#BSUB -B
### -- send notification at completion--
#BSUB -N
### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
#BSUB -o monodetr4_%J.out
#BSUB -e monodetr4_%J.err
# -- end of LSF options --

# -- load modules -- 
module load cuda/11.3
# -- end of load modules -- 

CUDA_VISIBLE_DEVICES=0 /work3/s222999/miniconda3/envs/monodetr/bin/python tools/train_val.py --config /work3/s222999/CubeDETR_3D/MonoDETR/configs/monodetr.yaml > logs/monodetr.log 