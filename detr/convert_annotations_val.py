import json

def kitti_to_coco(kitti_data):
    coco_format = {
        "info": {
            "description": "COCO 2017 Dataset",
            "url": "http://cocodataset.org",
            "version": "1.0",
            "year": 2017,
            "contributor": "COCO Consortium",
            "date_created": "2017/09/01"
        },
        "licenses": [
            {"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/", "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"},
            {"url": "http://creativecommons.org/licenses/by-nc/2.0/", "id": 2, "name": "Attribution-NonCommercial License"},
  
        ],
        "images": [],
        "annotations": [],
        "categories": []
    }

    for category in kitti_data["categories"]:
        coco_format["categories"].append({
            "id": category["id"],
            "name": category["name"],
            "supercategory": category.get("supercategory", "none")
        })
    

    image_id_map = {}
    for image in kitti_data["images"]:
        image_id_map[image["id"]] = len(coco_format["images"]) + 1  
        coco_format["images"].append({
            "license": 4, 
            "file_name": image["file_path"].split("/")[-1],
            "coco_url": "",
            "height": image["height"],
            "width": image["width"],
            "date_captured": "",
            "flickr_url": "",
            "id": image_id_map[image["id"]]
        })

    for annotation in kitti_data["annotations"]:
        image_id = image_id_map.get(annotation["image_id"], None)
        if image_id is None:
            continue  

        coco_format["annotations"].append({
            "segmentation": [],  
            "area": 0,  
            "iscrowd": 0,
            "image_id": image_id,
            "bbox": annotation["bbox2D_tight"],
            "category_id": annotation["category_id"],
            "id": annotation["id"]
        })

    return coco_format

 
kitti_data = json.load(open('/Users/aleksandra/Desktop/uni/3_Term/Advanced_Deep_Learning_in_Computer_Vision/CubeDETR_3D/detr/Coco_1/KITTI_val.json'))
coco_data = kitti_to_coco(kitti_data)
json.dump(coco_data, open('/Users/aleksandra/Desktop/uni/3_Term/Advanced_Deep_Learning_in_Computer_Vision/CubeDETR_3D/detr/Coco_1/coco_format_kitti_val.json', 'w'), indent=4)
