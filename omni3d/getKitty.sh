# kitti dataset
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip

# unzip image dataset
unzip data_object_image_2.zip -d datasets

# create directories for KITTI object dataset
mkdir -p datasets/KITTI_object/training/image_2
mkdir -p datasets/KITTI_object/testing/image_2

# move images to the appropriate directories
mv datasets/testing/image_2/* datasets/KITTI_object/testing/image_2
mv datasets/training/image_2/* datasets/KITTI_object/training/image_2

# clean up
rm -rf datasets/testing
rm -rf datasets/training
rm data_object_image_2.zip
