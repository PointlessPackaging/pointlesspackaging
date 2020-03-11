from mrcnn.model import log
import mrcnn.model as modellib
from mrcnn.visualize import display_images
import mrcnn.visualize as visualize
import mrcnn.utils as utils
from mrcnn.config import Config
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys
import json
import datetime
import skimage.draw
import cv2

# TODO: update this path
PP_WEIGHTS_PATH = "models/mask_rcnn_pointless_package_0050.h5"


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
    # Background + outerbox + innerbox + item_rect + item_rect_slim + item_sq + item_circ
    NUM_CLASSES = 1 + 6

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.75

class PPDataset(utils.Dataset):

    def load_dataset(self, dataset_dir, subset):
        """Load a subset of the Balloon dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        self.add_class("pointless_package", 1, "outerbox")
        self.add_class("pointless_package", 2, "innerbox")
        self.add_class("pointless_package", 3, "item_sq")
        self.add_class("pointless_package", 4, "item_rect")
        self.add_class("pointless_package", 5, "item_rect_slim")
        self.add_class("pointless_package", 6, "item_circ")

        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        # Load annotations
        # VGG Image Annotator (up to version 1.6) saves each image in the form:
        # { 'filename': '28503151_5b5b7ec140_b.jpg',
        #   'regions': {
        #       '0': {
        #           'region_attributes': {},
        #           'shape_attributes': {
        #               'all_points_x': [...],
        #               'all_points_y': [...],
        #               'name': 'polygon'}},
        #       ... more regions ...
        #   },
        #   'size': 100202
        # }
        # We mostly care about the x and y coordinates of each region
        # Note: In VIA 2.0, regions was changed from a dict to a list.
        annotations = json.load(
            open(os.path.join(dataset_dir, "via_region_data.json")))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]

        # Add images
        for a in annotations:
            # Get the x, y coordinaets of points of the polygons that make up
            # the outline of each object instance. These are stores in the
            # shape_attributes (see json format above)
            # The if condition is needed to support VIA versions 1.x and 2.x.
            if type(a['regions']) is dict:
                polygons = [r['shape_attributes']
                            for r in a['regions'].values()]
            else:
                polygons = [r['shape_attributes'] for r in a['regions']]

            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            class_list = [r['region_attributes'] for r in a['regions']]

            self.add_image(
                "pointless_package",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width, height=height,
                class_list=class_list,
                polygons=polygons)

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        class_ids = list()
        # If not a pointless_package dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        # if image_info["source"] != "pointless_package":
        #     return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        # print("\n\n\nIMAGE INFO:", info, "\n\n\n\n")

        for box_type in info['class_list']:
            # print(box_type['name'])
            class_ids.append(self.class_names.index(str(box_type['name'])))
        # print(class_ids)
        # print(self.class_names)

        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1
        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        return mask.astype(np.bool), np.asarray(class_ids, dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "pointless_package":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


config = PPConfig()
ROOT_DIR = os.getcwd()
PP_DIR = os.path.join(ROOT_DIR, "dataset/")

# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# Device to load the neural network on.
# Useful if you're training a model on the same
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"


def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax


MY_ABS_PATH = "./"
my_model_dir = MY_ABS_PATH + 'models/'

# Load validation dataset
dataset = PPDataset()
dataset.load_dataset(PP_DIR, "val")

# Must call before using the dataset
dataset.prepare()

print("Images: {}\nClasses: {}".format(
    len(dataset.image_ids), dataset.class_names))

# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=my_model_dir,
                              config=config)

# Set path to balloon weights file

# Download file from the Releases page and set its path
# https://github.com/matterport/Mask_RCNN/releases
# weights_path = "/path/to/mask_rcnn_balloon.h5"

# Or, load the last model you trained
# weights_path = model.find_last()[1]
weights_path = PP_WEIGHTS_PATH

# Load weights
print("Loading weights ", weights_path)
model.load_weights(weights_path, by_name=True)

# print(dataset.image_ids)
# image_id = random.choice(dataset.image_ids)
for number in range(150, 181):
    # image_id = number
    # image, image_meta, gt_class_id, gt_bbox, gt_mask =\
    #     modellib.load_image_gt(dataset, config, image_id, use_mini_mask=False)
    # info = dataset.image_info[image_id]
    # print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id,
                                        # dataset.image_reference(image_id)))

    image = cv2.imread('./dataset/val/IMG_'+str(number)+'.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run object detection
    results = model.detect([image], verbose=1)

    # Display results
    r = results[0]
    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                dataset.class_names, r['scores'],
                                title="Predictions")

    N = r['rois'].shape[0]
    class_ids = r['class_ids']
    masks = r['masks']

    class_names = np.asarray(dataset.class_names)

    print(class_names[class_ids])

    # score_card = [masks[:, :, i].sum() for i in range(N)]
    score_card2 = masks.sum(axis=0).sum(axis=0)
    # print(score_card)
    print(score_card2)
