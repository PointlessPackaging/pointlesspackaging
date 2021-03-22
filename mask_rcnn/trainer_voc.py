from xml.etree import ElementTree
from os import listdir
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
import mrcnn
from mrcnn.utils import Dataset
from mrcnn.model import MaskRCNN

import numpy as np
from numpy import zeros
from numpy import asarray
import colorsys
import argparse
import imutils
import random
import cv2
import os
import time

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.models import load_model

#inherting  from Config class

MY_ABS_PATH = "./"
PP_LABELS=[]

class PPConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "pointless_package"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 3  # Background + outerbox + innerbox + product

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

config = PPConfig()
config.display()

print("Loading Mask R-CNN model...")
my_model_dir = MY_ABS_PATH + 'models/'
model = modellib.MaskRCNN(
    mode="training", config=config, model_dir=my_model_dir)

#n load the weights for COCO
model.load_weights('./models/mask_rcnn_coco.h5',
                   by_name=True,
                   exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])
                   
model.keras_model.summary()


class PPDataset(Dataset):
    # load the dataset definitions
    def load_dataset(self, dataset_dir, is_train=True):

        # Add classes. We have only one class to add.
        self.add_class("dataset", 1, "outerbox")
        self.add_class("dataset", 2, "innerbox")
        self.add_class("dataset", 3, "product")

        # define data locations for images and annotations
        images_dir = dataset_dir + 'images/'
        annotations_dir = dataset_dir + 'annotations/'

        # Iterate through all files in the folder to
        #add class, images and annotaions
        for filename in listdir(images_dir):

            # extract image id
            image_id = filename[:-4]

            # skip bad images
            if image_id in ['00090']:
                continue
            # skip all images after 150 if we are building the train set
            if is_train and int(image_id[4:]) >= 150:
                continue
            # skip all images before 150 if we are building the test/val set
            if not is_train and int(image_id[4:]) < 150:
                continue

            # setting image file
            img_path = images_dir + filename

            # setting annotations file
            ann_path = annotations_dir + image_id + '.xml'

            # adding images and annotations to dataset
            self.add_image('dataset', image_id=image_id,
                           path=img_path, annotation=ann_path)

    # extract bounding boxes from an annotation file
    def extract_boxes(self, filename):

        # load and parse the file
        tree = ElementTree.parse(filename)
        # get the root of the document
        root = tree.getroot()
        # extract each bounding box
        boxes = list()
        for box in root.findall('.//object'):
            name = box.find('name').text
            xmin = int(box.find('.//bndbox').find('xmin').text)
            ymin = int(box.find('.//bndbox').find('ymin').text)
            xmax = int(box.find('.//bndbox').find('xmax').text)
            ymax = int(box.find('.//bndbox').find('ymax').text)
            coors = [xmin, ymin, xmax, ymax, name]
            boxes.append(coors)

        # for i, product in enumerate(root.findall('.//object')):
        #     name = product.find('name').text
        #     print(name)

        # extract image dimensions
        width = int(root.find('.//size/width').text)
        height = int(root.find('.//size/height').text)
        return boxes, width, height

    # load the masks for an image
    """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
     """

    def load_mask(self, image_id):
        # get details of image
        info = self.image_info[image_id]

        # define anntation  file location
        path = info['annotation']

        # load XML
        boxes, w, h = self.extract_boxes(path)

        # create one array for all masks, each on a different channel
        masks = zeros([h, w, len(boxes)], dtype=np.uint8)

        # create masks
        class_ids = list()
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index(box[4]))
        return masks, asarray(class_ids, dtype=np.int32)

    # load an image reference
    #Return the path of the image."""
    def image_reference(self, image_id):
        info = self.image_info[image_id]
        print(info)
        return info['path']


my_dataset_dir = MY_ABS_PATH + 'dataset/'

train_set = PPDataset()
train_set.load_dataset(
    my_dataset_dir, is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = PPDataset()
test_set.load_dataset(
    my_dataset_dir, is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))


# train weights (output layers or 'heads')
## train heads with higher lr to speedup the learning
model.train(train_set, test_set, learning_rate=config.LEARNING_RATE,
            epochs=5, layers='heads')

history = model.keras_model.history.history

model.get_trainable_layers()


model_path = MY_ABS_PATH + 'models/mask_rcnn_' + str(time.time()) + '.h5'
model.keras_model.save_weights(model_path)
