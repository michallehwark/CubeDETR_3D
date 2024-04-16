
# kitti dataset
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
# unzip 
unzip data_object_image_2.zip -d datasets
mkdir datasets/Kitti
mkdir datasets/Kitti/testing
mkdir datasets/Kitti/training
mv datasets/testing/image_2 datasets/Kitti/testing
mv datasets/training/image_2 datasets/Kitti/training
# clean
rm -rf datasets/testing
rm -rf datasets/training
rm data_object_image_2.zip
rm data_object_label_2.zip


# kitti labels in coco-like format 
wget https://dl.fbaipublicfiles.com/omni3d_data/Omni3D_json.zip
unzip Omni3D_json.zip
rm -r -f Omni3D_json.zip
rm -f datasets/Omni3D/AR*  
rm -f datasets/Omni3D/Hyper*
rm -f datasets/Omni3D/Object*
rm -f datasets/Omni3D/SUN*
rm -f datasets/Omni3D/nuSc*