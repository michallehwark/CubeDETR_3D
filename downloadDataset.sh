
# kitti dataset
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
# unzip 
unzip data_object_image_2.zip -d datasets
mkdir datasets/Kitti
mkdir datasets/Kitti/testing
mkdir datasets/Kitti/training
mv datasets/testing/image_2 datasets/Kitti/testing
mv datasets/training/image_2 datasets/Kitti/training

# labels 
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip
unzip data_object_label_2.zip -d datasets/Kitti/training_labels/
mv datasets/Kitti/training_labels/training/label_2 datasets/Kitti/training_labels/

# clean
rm -rf datasets/testing
rm -rf datasets/training
rm data_object_image_2.zip
rm data_object_label_2.zip