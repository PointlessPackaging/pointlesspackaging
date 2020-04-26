# Simple Flask app for running the Google Vision API in a web environment

This is a simple Flask app that runs our Google Vision API logic. The use of a
python virtual environment is recommended. Necessary packages can be installed
using `pip install -r requirement.txt`  

To run the server, simply run `python main.py`
and the server will run on `127.0.0.1:8080`

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


## Example usage
Check `static/js/app.js` for example on using
the API from JavaScript.

## Deployment
The API is deployed on the following Google Cloud instance:
`https://smallwebsite.nw.r.appspot.com/`. To invoked the API, simply make an
HTTP call to `https://smallwebsite.nw.r.appspot.com/find_retailer` or
`https://smallwebsite.nw.r.appspot.com/check_plastic` with the parameters
described in the API description heading above.
