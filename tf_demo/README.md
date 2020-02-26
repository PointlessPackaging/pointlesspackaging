# Tensorflow object detection API demo

I trained a network using the tensorflow object detection API using the dataset
that we created. It's pretty good at detecting boxes, but it does not detect the
product. If you wish to try it out, follow the instructions for getting it up
and running.

# Installing
Follow the steps to install the [tensorflow object detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md). **Important**: use Python 3.6 and tensorflow 1.15.00. The API
does not seem to support 2.0 yet, and I had issues with using Python 3.7 and
tensorflow 1.15. After installing, place the ```tf_demo``` directory under
```tensorflow/models```.

# Contents
```tf_demo``` contains the following structure:
```
tf_demo    
│
└───annotations # contains the csv annotation files and respective .record files
│   │   label_map.pbtxt #
│   │   test_labels.csv # csv file made from our xml annotations
│   │   test.record # generated for tensorflow
│   │   train_labels.csv # csv file made from our xml annotations
│   │   train.record # generated for tensorflow
└───eval # has evaluation metrics from running eval.py
└───images # this is our dataset
    └───train # training images and xml annotations
    └───test # test images and xml annotations
└───pre-trained-model # downloaded from tensorflow object detection API github.
└───trained-inference-graphs # contains .pb files to be used for evaluation
└───training # contains training checkpoints and config file
|   |   ssd_inception_v2_coco.config # important file that configures training
└───eval_img.py # visually displays detected boxes on a single image.
└───eval.py # creates evaluation metrics from the checkpoint on test data.
└───export_inference_graph.py # takes a checkpoint and makes an inference graph (model than can evaluate images)
└───train.py # run the model training
```

# Using this codebase
I followed a mix of tensorflow object detection API official [documentation](https://github.com/tensorflow/models/blob/master/research/object_detection) and a really good [tutorial](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html) to make it work.
