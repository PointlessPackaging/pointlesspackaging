# CREDIT FOR THIS LIBRARY: https://github.com/bendangnuksung/mrcnn_serving_ready

### MRCNN Model conversion
Script to convert [MatterPort Mask_RCNN](https://github.com/matterport/Mask_RCNN) Keras model to Tensorflow Frozen Graph and Tensorflow Serving Model.  
Plus inferencing with GRPC or RESTAPI using Tensorflow Model Server. 


### How to Run
1. Modify the path variables in 'user_config.py'
2. Run main.py
    ```bash
    python3 main.py
    ```
    
#### For Custom Config class
If you have a different config class you can replace the existing config in 'main.py'
```python
# main.py
# Current config load
config = get_config()

# replace it with your config class
config = your_custom_config_class

```

### Inferencing
Follow once you finish converting it to a `saved_model` using the above code

#### Tensorflow Model Server with GRPC and RESTAPI

1. First run your `saved_model.pb` in Tensorflow Model Server, using:
    ```bash
    tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=mask --model_base_path=/path/to/saved_model/
    ```
2. Modify the variables and add your Config Class if needed in `inferencing/saved_model_config.py`. No need to change if the saved_model is the default COCO model.
3. Then run the `inferencing/saved_model_inference.py` with the image path:
    ```bash
    # Set Python Path
    export PYTHONPATH=$PYTHONPATH:$pwd
   
    # Run Inference with GRPC
    python3 inferencing/saved_model_inference.py -t grpc -p test_image/monalisa.jpg
   
   # Run Inference with RESTAPI
    python3 inferencing/saved_model_inference.py -t restapi -p test_image/monalisa.jpg
    ```   

### Acknowledgement
Thanks to [@rahulgullan](https://github.com/rahulgullan) for RESTAPI client code.