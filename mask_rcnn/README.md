# Pointless Packaging W/ Mask R-CNN

MASK R-CNN: https://github.com/matterport/Mask_RCNN

```
DIRECTORY STRUCTURE
.
|____.gitignore
|____dataset
| |____train - contains all training images (in Google Drive)
| |____TRAIN-MINI.json - VIA annotations for training images
| |____val  - contains all vaidation images (in Google Drive)
| |____VAL-MINI.json - VIA annotations for validation images
| |____val_img_results - contains results of validation images after inference
| |____via.html - VIA annotator program
|____eval_on_val_set.py - performs inference on validation test, resuls in 
                          `val_img_results`
|____logs - training logs from the mask r-cnn library
|____models - contains trained models
| |____mask_rcnn_final.h5 (256MB) - DOWNLOAD LINK BELOW
| |____.gitkeep - Dummy file. Just ignore it.
|____mrcnn - matterport/Mask_RCNN library
|____README.md
|____requirements.txt
|____test_images - images that can be tested by running `score.py`
|____trainer.py - train a dataset using the Mask R-CNN library
|____trainer_voc.py - train a dataset in PASCAL-VOC format using the Mask R-CNN library
|
|____score.py - RUN THIS script to obtain scores of images 
                containing pointless packaging.
```

- Download trained model and place it in the `models/` directory.
    - ### <a href="https://drive.google.com/a/ucdavis.edu/file/d/1b82OoKjJksEZ0JZfZS4Y8DPK5VkSDVtp/view?usp=sharing" target="blank">CLICK HERE TO DOWNLOAD TRAINED MODEL</a>


## score.py
```
usage: score.py [-h] -m MODEL_SRC [-i IMG_SRC | -d DIR_SRC] [-v]

Simple script that takes a trained MASK R-CNN model (.h5), pointless
packaging image/images and then generates score of the packaging purely based on
the area of the package relative to the item inside; using the provided model.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_SRC, --model MODEL_SRC
                        Absolute/Relative path to the MASK R-CNN Model
  -i IMG_SRC, --img IMG_SRC
                        Absolute/Relative path of the image. Cannot include
                        --dir argument.
  -d DIR_SRC, --dir DIR_SRC
                        Absolute/Relative path of the directory containing the
                        images. Cannot include --img argument.
  -v, --visualize       Visualize the image.

```
### Example:
- Get score of a single image WITH visulatization.
    -  `python3 score.py -v -m models/mask_rcnn_final.h5 -i test_images/IMG_0.jpg`
- Get score for every single image in a directory WITH visualization.
    -  `python3 score.py -v -m models/mask_rcnn_final.h5 -d test_images/`
- Get score for every single image in a directory WITHOUT visualization.
    -  `python3 score.py -m models/mask_rcnn_final.h5 -d test_images/`

## TODO:
- Need to come up with a proper scoring function. 
  Currently, `score.py` gives only the area of the 
  box and items in pixels.