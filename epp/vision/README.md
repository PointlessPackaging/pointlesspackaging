# Instruction for Google cloud vision API
1. Team Email: 
    - email: eppecs193@gmail.com
    - password: ericecs199

2. Setting up your virtual environment
    - run `python3 -m venv venv3`
    - run `source venv3/bin/activate`
    
3. Install the Google Client Vision API client library
    - run `pip3 install --upgrade google-cloud-vision`
    - check whether installed, run `pip3 freeze | grep google-cloud-vision`
    
4. Set up credential on your local computer
    - Run `export GOOGLE_APPLICATION_CREDENTIALS="path/to/vision/google-vision.json"`

5. Test whether succeed setup
    - Run `python3 test_setup.py`
    
Additional resources:
https://towardsdatascience.com/tutorial-google-vision-api-with-python-and-heroku-3b8d3ff5f6ef


