# Google Vision API for eliminating pointless packaging
This is short documentation on using the Google Vision API to detect pointless packaging.

## Setting up
In order to use the Google Vision API, it is necessary to set up a Google Cloud project. Follow the Google  [documentation](https://cloud.google.com/vision/docs/libraries#client-libraries-install-python) to set it up.  

I recommend using a virtual environment to install the dependencies. Run `pip install -r requirements.txt` inside your [virtual environment](https://docs.python.org/3/tutorial/venv.html) to set up your dependencies.

# Usage
The Python file `image_analyzer.py` contains two function that are useful for using the Google Vision API. Simply import it as such to use the functions: `import image_analyzer` to use the functions. The functions are:
* check_plastic() which checks for plastic content.
* call_Vision_API() which is a wrapper around the API call with custom features.

Check function description for arguments and returns values.
