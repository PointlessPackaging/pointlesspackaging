# Your Inference Config Class
# Replace your own config
# MY_INFERENCE_CONFIG = YOUR_CONFIG_CLASS
# import coco
# class InferenceConfig(coco.CocoConfig):
#     GPU_COUNT = 1
#     IMAGES_PER_GPU = 1
# coco_config = InferenceConfig()
import pp_api.api.mrcnn_inference.config as config
class PPConfig(config.Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "pointless_package"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.75

MY_INFERENCE_CONFIG = PPConfig()


# Tensorflow Model server variable
ADDRESS = 'localhost'
PORT_NO_GRPC = 8500
PORT_NO_RESTAPI = 8501
MODEL_NAME = 'mask'
REST_API_URL = "http://%s:%s/v1/models/%s:predict" % (ADDRESS, PORT_NO_RESTAPI, MODEL_NAME)


# TF variable name
OUTPUT_DETECTION = 'mrcnn_detection/Reshape_1'
OUTPUT_CLASS = 'mrcnn_class/Reshape_1'
OUTPUT_BBOX = 'mrcnn_bbox/Reshape'
OUTPUT_MASK = 'mrcnn_mask/Reshape_1'
INPUT_IMAGE = 'input_image'
INPUT_IMAGE_META = 'input_image_meta'
INPUT_ANCHORS = 'input_anchors'
OUTPUT_NAME = 'predict_images'


# Signature name
SIGNATURE_NAME = 'serving_default'

# GRPC config
GRPC_MAX_RECEIVE_MESSAGE_LENGTH = 4096 * 4096 * 3 # Max LENGTH the GRPC should handle
