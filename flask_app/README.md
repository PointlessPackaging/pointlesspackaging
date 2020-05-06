# Simple Flask app for running the Google Vision API in a web environment

This is a simple Flask app that runs our Google Vision API logic. The use of a
python virtual environment is recommended. Necessary packages can be installed
using `pip install -r requirements.txt`  

The server has two options to run. One on the cloud, and the other locally.
To run the server locally, simply run `python main.py`--local
and the server will run on `127.0.0.1:8080`
Running it on the cloud requires root access.

**Note:** when running locally, Google Cloud account credentials need to be
enabled: follow instructions [here](https://cloud.google.com/vision/docs/libraries).

# API description
## Retailer identification
The expected route is '/find_retailer' and the
expected data is a filed 'side_view' that
contain image data. The response is in JSON
format and it contains a field 'retailer'
which contains the retailer name.  

## Plastic identification
The expected route is '/check_plastic' and the
expected data is a filed 'side_view' that
contain image data. The response is in JSON
format and it contains a field 'has_plastic'
which is a True/False value.

## Materials identification
The expected route is '/find_materials' and the
expected data is a filed 'side_view' that
contain image data. The response is in JSON
format and it contains four name/value pairs:
- has_plastic : True/False
- has_paper : True/False
- has_carton : True/False
- has_cardboard : True/False

## Example usage
Check `static/js/app.js` for example on using
the API from JavaScript.

## Deployment
The API is deployed on a VM instance in Google Cloud with the IP 34.71.6.144.
 To invoke the API, simply make an HTTP call to `http://34.71.6.144/find_retailer` or
`http://34.71.6.144/check_plastic` or
`http://34.71.6.144/find_materials` with the parameters
described in the API description heading above.
