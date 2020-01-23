Meeting began at 1:10pm over Google Hangouts.
# Objective
We came together to find out what our current understanding of the project is and to formulate questions for Eric during the client meeting.

# Current Project Understanding
We will be developing a website that will be grading retailers based on their packaging practices. The website will get data by crawling through social media posts and looking for reviews/posts that show examples of good/bad examples of packaging. The way we identify whether a post shows packaging practices will be by processing their text and images. For that purpose, we will need to develop text analysis and computer vision algorithms that will identify relevant posts.

# Current understanding of Infrastructure/Architecture:
We will need to use a cloud service such as AWS/Google Cloud to run our web crawling/data collection algorithms and collect data there. If we need to train computer vision/machine learning models to help us recognize plastic in images, we will also do this on a cloud based service because we do not have such strong GPUs.

# Questions for Eric
* What is his knowledge/experience in software engineering?
* What does the end product look like?
  * Is it a website that is updated all the time as our algorithms collect data, or do we just present data that we accumulated for the duration of our project?
  * How many companies should we focus on?
  * With the massive amounts of data coming for each company, how are we going to grade a company? If this is too difficult of a task, do we just present the reviews that we have extracted?
* What are the moving parts of this project and what is the architecture from a high level?
  * Where are our algorithms (vision and text) for recognizing relevant reviews running, and where do we accumulate data?
  * What kind of machine learning / computer vision methods should we use to detect plastic in images in review posts?
* What kind of data are we looking for and how do we get it?
  * Our current understanding is that we will be crawling through customer reviews. Is there an example of a review that would be ideal for our project?
  * What are the types of reviews are we looking to extract?
  * What are the techniques that we can use to recognize that a review is what we need?
* How many sources of data would be good? (Assuming an example of a data source is Facebook API, Twitter API etc…)
* This question links to one of the previous questions, but how scalable should this be?


Meeting concluded at 1:50pm.
