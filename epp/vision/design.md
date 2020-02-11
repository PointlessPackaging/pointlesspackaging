
## Thoughts:

1. Object detection is not necessary if we are using labels detection (since we are looking for the same key words, box and packaging). Besides "box" and "packaging", lables detection gives us more desired key words, such as Cardboard, Paper product and  Room.

2. Another problem of object detection is that, Google vision API would not necessily recognized the "product" in the middle of the box, because it is not a specific object. I suggest that we should rethink about object detection, which also applies to our neural network development.

3. Beside detecing "what," the next thing we what is "how much." We could achieve this by detect the 


## System Design:

1. User Lable deteciton to: 
    - construct a desired key words collection
    - display a predefined key-word-table with check marks.    
    
2.  (Optional) Transiiton step
    - crop the backgroud boundary section

3. User properties Detection to:
    - Define a range of RGB acceptance in advance
    - Sum the percemtage with RBG acceptance 
    - Output the usage ratio of the packaging, which is this sum. 

## Demo Output
# =======================
# Labels:
# Cardboard +
# Carton
# Footwear
# Paper +
# Paper product +
# Room +
# Packaging and labeling +
# Shoe
# Plastic bag +
# Paper bag +
# =======================
# Labels:
# Plastic
# Plastic wrap
# Plastic bag
# Material property
# Carton
# Packaging and labeling
# Box
# Package delivery
# =======================
# Labels:
# Transparency
# Box
# Electronics
# Packing materials
# Packaging and labeling
# Plastic
# =======================
# Labels:
# Wood
# Toilet
# Plywood
# Cardboard
# Room
# Table
# Floor
# Stairs
# Furniture
# Toilet seat

## Table
1. Matter
Packaging
Box

2. Materials
Cardboard
Paper
Plastic

3. Spacial 
Room --> spacial ratio