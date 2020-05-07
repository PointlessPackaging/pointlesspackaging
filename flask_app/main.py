'''
This Flask server serves the image_analyzer library which wraps the Google
Vision API and identifies the retailer, checks for plastic content, and finds
all materials in the returned labels.
'''

from datetime import datetime
import logging
import os
import argparse

from flask import Flask, redirect, render_template, request, jsonify
from flask_cors import CORS, cross_origin


from google.cloud import vision

import image_analyzer as ia

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    # Return a Jinja2 HTML template
    return render_template('homepage.html')


@app.route('/find_retailer', methods=['GET', 'POST'])
@cross_origin()
def find_retailer():
    print("triggered")
    try:
        photo = request.files['side_view'].read()
    except:
        return {'error' : "bad side_view file"}, 400

    retailer = ia.find_retailer(photo)
    response = {'retailer' : retailer}

    return jsonify(response), 200

@app.route('/check_plastic', methods=['GET', 'POST'])
@cross_origin()
def check_plastic():
    try:
        photo = request.files['side_view'].read()
    except:
        return {'error' : "bad side_view file"}, 400

    has_plastic = ia.check_plastic(photo)
    response = {'has_plastic' : has_plastic}

    return jsonify(response), 200

@app.route('/find_materials', methods=['GET', 'POST'])
@cross_origin()
def find_materials():
    try:
        photo = request.files['side_view'].read()
    except:
        return {'error' : "bad side_view file"}, 400

    returned_materials = ia.find_materials(photo)

    response = {
        'has_plastic' : False,
        'has_paper' : False,
        'has_paperboard' : False,
        'has_cardboard' : False
    }

    for material in returned_materials:
        if material is 'plastic':
            response['has_plastic'] = True
        elif material is 'paper':
            response['has_paper'] = True
        elif material is 'paperboard':
            response['has_paperboard'] = True
        elif material is 'cardboard':
            response['has_cardboard'] = True

    return jsonify(response), 200

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check to run locally or not")
    parser.add_argument("--local", action='store_true', dest='local', \
            help='Add flag if you want to run app locally. Otherwise requires \
            running in sudo')
    args = parser.parse_args()
    # run locally
    if args.local:
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=80, debug=True)
