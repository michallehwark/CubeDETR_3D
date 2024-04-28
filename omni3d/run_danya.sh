# train 
python tools/train_net.py --config-file configs/Base_Omni3D_kitti.yaml OUTPUT_DIR output/omni3d_example_run
# train with 1 gpu 
python tools/train_net.py --config-file configs/Base_Omni3D_kitti2.yaml --num-gpus 1 OUTPUT_DIR output/omni3d_baseline2 > baseline2_train.log

# evaluate 
python tools/train_net.py --eval-only --config-file configs/Base.yaml MODEL.WEIGHTS output/omni3d_baseline/baseline_best_ckpt.pth OUTPUT_DIR output/omni3d_baseline/evaluation
