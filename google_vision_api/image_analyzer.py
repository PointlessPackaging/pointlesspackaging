#!/usr/bin/python3
'''
This program reads the command line argument and makes a call to the Google
Vision API. After that, it does some analysis on the image content.
'''

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Define a dictionary
labels = {
    'label_detection' : types.Feature.LABEL_DETECTION,
    'crop_hints' : types.Feature.CROP_HINTS,
    'text_detection' : types.Feature.TEXT_DETECTION,
    'face_detection' : types.Feature.FACE_DETECTION,
    'image_properties' : types.Feature.IMAGE_PROPERTIES,
    'landmark_detection' : types.Feature.LANDMARK_DETECTION,
    'logo_detection' : types.Feature.LOGO_DETECTION,
    'object_localization': types.Feature.OBJECT_LOCALIZATION,
    'web_detection': types.Feature.WEB_DETECTION
}

top_retailers = ['Amazon', 'Apple', 'Dell', 'Walmart', 'Target', 'Autozone']

def load_image(file_name):
    '''
    Loads a local images into a Google Vision Image type.
    Arguments:
        - file_name: path to image

    Returns: Google Vision Image type.
    '''
    assert isinstance(file_name, str), 'Expected str type for file_name.'

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    return image

def call_Vision_API(image_path, requested_features):
    '''
    Wrapper around the Google Vision API. Enables calling it in one line
    with image path and requested features.
    Arguments:
        - image_path: path to image
        - requested_features: array of strings with features requested.

    Returns: AnnotateImageResponse. Check the README for more info on this type.
    '''
    assert isinstance(image_path, str), 'image_path should be a string.'
    assert isinstance(requested_features, list), 'requested_features should be \
            a list.'

    # load the image
    image = load_image(image_path)

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    all_features = []

    # Attach all the features caller requested
    for request in requested_features:
        if request not in labels:
            print(request, "is not a valid feature.")

        # append feature to the list of features to be requested
        feature_type = labels[request]
        feature = types.Feature(type=feature_type, max_results=10)
        all_features.append(feature)

    # create the request
    request = types.AnnotateImageRequest(image=image, \
                    features=all_features)

    # call the image annotation
    result = client.annotate_image(request)

    return result

def check_plastic(image_path):
    '''
    Calls the Google Vision label detection and checks if plastic has been
    found.
    Arguments:
        - image_path: path to image

    Returns: True if plastic is present in image, False if plastic is not
        present.
    '''
    api_result = call_Vision_API(image_path, ['label_detection'])

    if not api_result.label_annotations:
        return False

    for label in api_result.label_annotations:
        label = label.description
        label = label.lower()
        if 'plastic' in label:
            return True

    return False

def logo_OCR(image_path):
    '''
    Attempts to identify the retailer based on text detection.
    Arguments:
        - image_path: path to image

    Returns: String with retailer name if retailer found. NoneType if none is
    found.
    '''
    # try to run logo detection
    api_result = call_Vision_API(image_path, ['text_detection'])

    if not api_result.text_annotations:
        return None

    for annotation in api_result.text_annotations:
        # extract string
        text = annotation.description
        # remove formatting
        text = text.lower()
        text = text.replace(' ', '')

        for retailer in top_retailers:
            if retailer.lower() in text:
                return retailer

    return None

def find_retailer(image_path):
    '''
    Calls the Google Vision API logo detection and tries to find retailer.
    Arguments:
        - image_path: path to image

    Returns: String with retailer name if retailer found. NoneType if none is
    found.
    '''
    # try to run logo detection
    api_result = call_Vision_API(image_path, ['logo_detection'])

    # logo could not be found, try OCR
    if not api_result.logo_annotations:
        return logo_OCR(image_path)

    for annotation in api_result.logo_annotations:
        if annotation.score > 0.8:
            return annotation.description

    return logo_OCR(image_path)
