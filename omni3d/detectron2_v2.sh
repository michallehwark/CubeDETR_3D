#!/bin/sh
### General options
### –- specify queue --
# BSUB -q gpua100
### -- set the job Name --
# BSUB -J decetron2
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
# BSUB -o detectron2_v2%J.out
# BSUB -e detectron2_v2%J.err
# -- end of LSF options --

# -- load modules -- 
module load cuda/10.2
# -- end of load modules -- 

# Setup new environment
echo "Creating Conda environment..."
conda create -y -n test3 python=3.8

# Activate the Conda environment
echo "Activating Conda environment..."
source activate test3

# Install main dependencies
echo "Installing main dependencies..."
conda install -y -c fvcore -c iopath -c conda-forge -c pytorch3d -c pytorch fvcore iopath pytorch3d pytorch==1.8.0 torchvision=0.9.0 cudatoolkit=10.2

# Install OpenCV, COCO, detectron2
echo "Installing additional dependencies..."
pip install cython opencv-python

python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.8/index.html

# Install other dependencies
echo "Installing other dependencies..."
conda install -y -c conda-forge scipy seaborn

echo "Setup completed."
echo "Let's try to run detectron2 :)"

module load cuda/10.2
# Run an example demo
/zhome/df/0/181554/miniconda3/envs/test3/bin/python ./demo/demo.py \
--config-file cubercnn://omni3d/cubercnn_DLA34_FPN.yaml \
--input-folder "datasets/coco_examples" \
--threshold 0.25 --display \
MODEL.WEIGHTS cubercnn://omni3d/cubercnn_DLA34_FPN.pth \
OUTPUT_DIR output/demo

echo "It run correctly!"



