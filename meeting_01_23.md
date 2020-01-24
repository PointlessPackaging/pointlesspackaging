Meeting 1520 23 Jan 2020

# Background
First meeting with client.

# Project Scope
* Website
* Rank big manufacturer 
    - Cheetos
    - Coca Cola
* Rank big retailers
    - Amazon
    - Etsy
    - Walmart

# Technical Challenges
* **Computer vision**
    - Recognize the company with computer vision
    - Quantify how much plastic
* How do we recognize if there is excess plastic?
    * See an item that is a small but in a big package
    * See something that doesn't need a lot of packaging but is packaged 
    excessively
    * Does not need any packing material except for paper
+ Text recognition could be a challenge
    * Amazon grocery stores is an example of this problem solved

# Ideas
* Compare the product dimensions with the size of the box
    - Could get the size of the product from the website itself
    - OR try to determine the dimensions from the photo itself
* May have to build our own neural network
    - Would need to train it
    - Yoosuf has experience training neural networks
* Texture of cardboard is unique
    - Should be easy to identify 
* Ask people to post pictures of their product in its package
    - Create the testing dataset
    - Real world dataset
* Will be very likely working with *openCV*
* AWS or Google for APIs

## Data Base
* Just looking to prove it
* For now it just has to work
* Maybe start with a *file system*
    - Use Dropbox or something

# Goal
* Doesn't have to be perfect
* Prove we can do it
* Recognize the manufacturer with a picture
* Figure out brand and retailer
* Confirm if the packaging is good
* We are trying to educate people on the environmental impact of their packaging
* Our goal is to capture the attention of the companies 

# Future Steps
* Build a test set of images
    - Web scrape images
    - We already have some photos
* Get the retailer name
* Judge whether the packaging is good
    - Detect packaging
    - Measure the size of the box and compare it to the overall size of the 
    product
* After the algorithm is created then we can begin getting more data from the 
web

## Short Term Goals (5 Weeks)
* Have a neural network decided on and tested
* Have a test set of data

# Future Meetings
* Have a weekly meeting setup
* Evenings Tuesday through Thursdays
    * Phone call each week
+ Occasional in person meeting

* *Capture my meeting* on Youtube 
    - Former senior design project that is similar to ours

Meeting finished at 



