# Pointless Packaging App Documentation

## How to run the app locally:

### Starting the DJANGO app
0. Delete any `db.sqlite3` if it exists in `server` folder.
1. Open up the terminal in this directory and `cd server`
2. `python manage.py migrate authtoken`
3. `python manage.py migrate`
    - Do not delete the migrations that is already setup in the `accounts` app before running this.
    - This will create the superuser for you.
    - Default Superuser info for login:
        - `username='admin@pp.com', password='password'`
        - You should change this information in production. 
    - This will seed 40 of the most common brands with `score` and `count` choson at random. For more information, checkout out `server/pp_api/migrations/pp0002_initpackager_20200429_0854.py`
4. `python manage.py runserver`

If you have already made the migrations, skip step 2 and 3.

The API should be running! But we are not yet done with the setup as we have to setup the Mask R-CNN.

### Starting the Mask R-CNN API

There are two options. Setup the API locally or directly call the cloud model.
#### Setting up locally (skip this if you are using the cloud API):
1. Download the serving model from this location and unzip it anywhere:
    - <a href="https://drive.google.com/a/ucdavis.edu/file/d/19xC4ZLuyJwEjzARPC2Ky859YrEqmf57o/view?usp=sharing">CLICK HERE</a>
2. Install <a href="https://www.tensorflow.org/tfx/serving/setup">Tensorflow Serving (TFS)</a>
    - For MAC users: I am not sure whether this can be done easily. Though I am pretty sure you have to use Docker to install TFS. It is a bit more complicated than in installing in Linux.
    - For Linux users: Follow the steps outlined in the link above.
3. Run the tensorflow model server locally so you can make RPC requests.
    - `tensorflow_model_server --port=8500 --model_name=mask --model_base_path=/absolute/path/to/model/serving_model`

#### Setting up in the cloud:
1. Already setup. However, the servers are not always on due to cost reasons.

#### Connecting Django and M-RCNN:
1. Open up `server/settings.py`.
2. Comment/Uncomment `MASK_RCNN_API_IP` variable for cloud or local based on your needs. Default is set to local machine.

And...you are done! In terms of setting up at least...

## Using POSTMAN to make UNAUTHENTICATED requests (Updated):
1. `POST` with http://localhost:8000/api/upload - with 'Body' keys and values.
    - The `key`s are: `email`, `packager`, **`top_img`, **`side_img`
    - ** make sure you select 'File' in the Key drop down meny for these.
    - Click on send. The image should be uploaded and the inference score should given.
2. `GET` with http://localhost:8000/api/display_feed?page=1 to display all uploaded images.

## Other information:
- `localhost:8000` can be replaced with `pointlesspackaging.space` if accessing the cloud server.
- Accessing the admin page: `http://localhost:8000/admin` and login as a superuser to have control.

## Warnings:
- Do not mess around with the `accounts` app migration unless you know what you are doing.

## Credits:
- (For code used in M-RCNN inference part of this app) https://github.com/bendangnuksung/mrcnn_serving_ready
- (Used this to learn the DJANGO Rest Framework) https://github.com/mitchtabian/CodingWithMitchBlog-REST-API

## Some sources:
- https://docs.djangoproject.com/en/3.0/
- (Making DB queries) https://docs.djangoproject.com/en/3.0/topics/db/queries/
- https://www.django-rest-framework.org/
- https://www.youtube.com/playlist?list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV
- (What is ORM?) https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a