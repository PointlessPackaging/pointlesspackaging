# Google Vision API for eliminating pointless packaging
This is short documentation on using the Google Vision API to detect pointless packaging.

## Setting up
In order to use the Google Vision API, it is necessary to set up a Google Cloud project. Follow the Google  [documentation](https://cloud.google.com/vision/docs/libraries#client-libraries-install-python) to set it up.  

I recommend using a virtual environment to install the dependencies. Run `pip install -r requirements.txt` inside your [virtual environment](https://docs.python.org/3/tutorial/venv.html) to set up your dependencies.

## image_analyzer.py
This package is set up as an executable but it's functions can be used to extract the following information from an image:
* Plastic content
* Retailer information

To try it, run `python3 image_analyzer.py -h`
