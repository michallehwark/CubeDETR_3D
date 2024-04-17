# module load cuda/11.6
# module load matplotlib/3.7.4-numpy-1.24.4-python-3.8.18
# module load pandas/2.0.3-python-3.8.18
# module load cython/3.0.6-python-3.8.18
# module load scipy/1.10.1-python-3.8.18

# detr model requires numpy<1.24
module purge 
module load cuda/11.6
module load matplotlib/3.6.0-numpy-1.23.3-python-3.8.14
module load pandas/1.4.4-python-3.8.14
module load cython/0.29.32-python-3.8.14
module load scipy/1.9.1-python-3.8.14

virtualenv adlcv2
source adlcv2/bin/activate

pip3 install torch 
pip3 install torchvision
pip3 install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
