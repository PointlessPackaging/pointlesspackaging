Team meeting at 1815 12 February 2020

# Updates
- openCV
    + Edge detection
    + k means clustering

Learned the limits of traditional computer vision. We have learned why people 
use neural networks. 

# Plans
- Isolate calls to save costs
    1. Logo detection
    2. OCR
    3. Label detection
- Get Filip's PR up
- Move towards training the neural network

# Steps for training NN
1. Collect data ~500 images
    * At least 300
    * Take a picture over a box
    * One object in the box for now
    * Will need a new data set for when we add plastic
    * Use an image label tool
        - Draw rectangle for box and label it box
        - Draw rectangle around product and call it product
            + Returns .xml file
    * Put this into image AI and then have it train that

# By next meeting
* Each have taken 70 pictures by Saturday night/Sunday morning
    - Label them carefully
    - Try to get it top down, but the angle should not matter
        + Do not take the picture at a bad angle
* Try plugging it into the neural network code
    - Use ImageAI
        + Pretrained NN for object detection
    - Find out how long it takes to train
    - Find out if it can be done on a laptop
    - See if it actually works

Our goal it to get our confidence up when using a neural network. 

Meeting concluded at 1900 on 12 February 2020.
