#!/bin/bash -e
# -*- coding: utf-8 -*-
# Copyright (c) Meta, Inc. and its affiliates. All Rights Reserved

# get coco dataset 
wget http://images.cocodataset.org/zips/val2017.zip
unzip val2017.zip
rm -f val2017.zip
mkdir datasets/COCO
mv val2017 datasets/COCO/

# get coco annotations
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip annotations_trainval2017.zip
rm -f annotations_trainval2017.zip
mv annotations datasets/COCO/