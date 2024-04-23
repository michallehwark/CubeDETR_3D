import json
import os

def kitti_to_coco(kitti):
    # Convert KITTI data to COCO format
    coco = {
        "info": {
            "description": "COCO 2017 Dataset",
            "url": "http://cocodataset.org",
            "version": "1.0",
            "year": 2017,
            "contributor": "COCO Consortium",
            "date_created": "2017/09/01"
        },
        "licenses": [
            {"url": "http://creativecommons.org/licenses/by/2.0/", "id": 1, "name": "Attribution License"}
        ],
        "images": []
    }

    for img in kitti["images"]:
        coco_img = {
            "license": 1,
            "file_name": img["file_path"].split("/")[-1],
            "coco_url": "http://example.com/" + img["file_path"],
            "height": img["height"],
            "width": img["width"],
            "date_captured": "2013-11-14 17:02:52",
            "flickr_url": "http://example.com/" + img["file_path"],
            "id": img["id"]
        }
        coco["images"].append(coco_img)

    return coco

def convert_and_save_json_files(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file_name in os.listdir(source_folder):
        if file_name.endswith('.json'):
            source_file_path = os.path.join(source_folder, file_name)
            
            with open(source_file_path, 'r') as file:
                kitti_data = json.load(file)
            
            coco_data = kitti_to_coco(kitti_data)

            target_file_path = os.path.join(target_folder, file_name)
            with open(target_file_path, 'w') as file:
                json.dump(coco_data, file, indent=4)
            
            print(f'Converted and saved: {file_name}')

source_folder = '/work3/s223216/CubeDETR_3D/datasets/Kitti/annotations'
target_folder = '/work3/s223216/CubeDETR_3D/datasets/Kitti/annotations_2'
convert_and_save_json_files(source_folder, target_folder)
