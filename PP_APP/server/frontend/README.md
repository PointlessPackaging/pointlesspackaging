# How To Run

This is the source files for the website design. To run the website **leave** this 
directory and go to the *PP_APP/server* directory. Make sure that you are running 
within your virtual environment with *requirements.txt*. Then run:

``
    python manage.py runserver
``

Then open up *localhost:8000/home* in any browser.


The website will be running. You can check things by resizing the window, the navbar
is designed to shrink along with it. You can also click on all links. However, the 
links associated with the table do not work.

# Reference

## Pages

*base.html*: this is the main theme. It contains the navigation bar, footer, and 
imports for the *.css* script. This is inherited by all other pages.

## Styling

*main.css*: is a compiled *.css* file containing all of the bootstrap classes with 
some modifications that I added. The modifications can be found in *main.scss*.

*style.css*: contains classes I created that were **NOT** based on *Bootstrap*.

*images*: is a directory under *static/css* which contains all the images needed 
to run the website.

