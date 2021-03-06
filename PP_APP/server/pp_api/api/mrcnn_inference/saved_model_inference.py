import warnings
warnings.filterwarnings("ignore")
import cv2, grpc
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis import predict_pb2
import numpy as np
import tensorflow as tf
import pp_api.api.mrcnn_inference.saved_model_config as saved_model_config
from pp_api.api.mrcnn_inference.saved_model_preprocess import ForwardModel
import requests
import json
from pp_api.api.mrcnn_inference.visualize import display_images
import pp_api.api.mrcnn_inference.visualize as visualize
from django.conf import settings
import os
import requests
import base64
import re

host = saved_model_config.ADDRESS
PORT_GRPC = saved_model_config.PORT_NO_GRPC
RESTAPI_URL = saved_model_config.REST_API_URL

channel = grpc.insecure_channel(str(host) + ':' + str(PORT_GRPC), options=[('grpc.max_receive_message_length', saved_model_config.GRPC_MAX_RECEIVE_MESSAGE_LENGTH)])

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


request = predict_pb2.PredictRequest()
request.model_spec.name = saved_model_config.MODEL_NAME
request.model_spec.signature_name = saved_model_config.SIGNATURE_NAME

model_config = saved_model_config.MY_INFERENCE_CONFIG
preprocess_obj = ForwardModel(model_config)


def detect_mask_single_image_using_grpc(image):
    images = np.expand_dims(image, axis=0)
    molded_images, image_metas, windows = preprocess_obj.mold_inputs(images)
    molded_images = molded_images.astype(np.float32)
    image_metas = image_metas.astype(np.float32)
    # Validate image sizes
    # All images in a batch MUST be of the same size
    image_shape = molded_images[0].shape
    for g in molded_images[1:]:
        assert g.shape == image_shape, \
            "After resizing, all images must have the same size. Check IMAGE_RESIZE_MODE and image sizes."

    # Anchors
    anchors = preprocess_obj.get_anchors(image_shape)
    anchors = np.broadcast_to(anchors, (images.shape[0],) + anchors.shape)

    request.inputs[saved_model_config.INPUT_IMAGE].CopyFrom(
        tf.contrib.util.make_tensor_proto(molded_images, shape=molded_images.shape))
    request.inputs[saved_model_config.INPUT_IMAGE_META].CopyFrom(
        tf.contrib.util.make_tensor_proto(image_metas, shape=image_metas.shape))
    request.inputs[saved_model_config.INPUT_ANCHORS].CopyFrom(
        tf.contrib.util.make_tensor_proto(anchors, shape=anchors.shape))

    result = stub.Predict(request, 60.)
    result_dict = preprocess_obj.result_to_dict(images, molded_images, windows, result)[0]
    return result_dict


def detect_mask_single_image_using_restapi(image):
    images = np.expand_dims(image, axis=0)
    molded_images, image_metas, windows = preprocess_obj.mold_inputs(images)

    molded_images = molded_images.astype(np.float32)

    image_shape = molded_images[0].shape

    for g in molded_images[1:]:
        assert g.shape == image_shape, \
            "After resizing, all images must have the same size. Check IMAGE_RESIZE_MODE and image sizes."

    anchors = preprocess_obj.get_anchors(image_shape)
    anchors = np.broadcast_to(anchors, (images.shape[0],) + anchors.shape)

    # response body format row wise.
    data = {'signature_name': saved_model_config.SIGNATURE_NAME,
            'instances': [{saved_model_config.INPUT_IMAGE: molded_images[0].tolist(),
                           saved_model_config.INPUT_IMAGE_META: image_metas[0].tolist(),
                           saved_model_config.INPUT_ANCHORS: anchors[0].tolist()}]}

    response = requests.post(RESTAPI_URL, data=json.dumps(data), headers={"content-type":"application/json"})
    result = json.loads(response.text)
    result = result['predictions'][0]

    result_dict = preprocess_obj.result_to_dict(images, molded_images, windows, result, is_restapi=True)[0]
    return result_dict

def do_prediction(image_path):
    if settings.DEBUG:
        image = cv2.imread(settings.BASE_DIR+image_path)
    else:
        """ Download from the storage server onto the ram """
        resp = requests.get(image_path, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if image is None:
        print("Image path is not proper")
        exit()
    
    result = detect_mask_single_image_using_grpc(image)
    r = result

    class_ids = r['class']
    masks = r['mask']

    CLASS_NAMES = ['BG', 'outerbox', 'innerbox', 'item',
                   'item', 'item', 'item']

    class_names = np.asarray(CLASS_NAMES)
    area_occupation = masks.sum(axis=0).sum(axis=0)

    infer_img = visualize.display_instances(image, r['rois'], r['mask'], r['class'],
                                    CLASS_NAMES, r['scores'],
                                    title="Predictions")
                                    
    infer_img = cv2.cvtColor(infer_img, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', infer_img)
    infer_b64_img = base64.b64encode(buffer)
    return infer_b64_img, dict(zip(class_names[class_ids], area_occupation))
