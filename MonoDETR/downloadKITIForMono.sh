
# kitti dataset
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
# unzip 
unzip data_object_image_2.zip -d datasets
mkdir data/KITTIDataset
mkdir data/KITTIDataset/testing
mkdir data/KITTIDataset/training
mv datasets/testing/image_2 data/KITTIDataset/testing
mv datasets/training/image_2 data/KITTIDataset/training

# labels 
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip
unzip data_object_label_2.zip -d data/KITTIDataset/training_labels/
mv data/KITTIDataset/training_labels/training/label_2 data/KITTIDataset/training_labels/

# clean
rm -rf datasets/testing
rm -rf datasets/trainig
rm data_object_image_2.zip
rm data_object_label_2.zip