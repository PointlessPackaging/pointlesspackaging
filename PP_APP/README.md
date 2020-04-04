# Pointless Packaging App Documentation

# Running the App:

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
    - <a href="https://drive.google.com/a/ucdavis.edu/file/d/19xC4ZLuyJwEjzARPC2Ky859YrEqmf57o/view?usp=sharing" target="_blank">CLICK HERE</a>
2. Install <a href="https://www.tensorflow.org/tfx/serving/setup" target="_blank">Tensorflow Serving (TFS)</a>
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

---
# API

## Calls:
##### \* - strictly required.
##### Pagination: Dividing the results into pages. This feature is useful if there are a lot of results. If there are a million results for our search, we don't want to load them all right away. We want to get them in pages. ONLY 10 RESULTS are allowed per page. This can be changed in `server/server/settings.py`. The typical response will look like this: (`count`, `next`, `previous`, `results[]`) where `results` array contains the actual search results. `count` describes how many of results are there. However, not all results are displayed at once since the the response is paginated. `previous` and `next` gives you the link the get the previous/next page of the results. If there is no previous/next page, the value for them will be `null`. See "Other Information" section for an example.

- `/api/upload`
    - Request type: `POST`
    - Request body: (*`email`, *`top_img`, *`side_img`)
    - Response body: (`post_id`, `infer_img`, `outer_size`, `inner_size`, `item_size`)
    - Description: `email` must be a valid email address. `top_img` and `side_img` must be images of bad packaging. Once the response is received from this call and Google Vision API (GV), a score will be calculated on the client side using Javascript. Using the score, GV data, `/api/update` **must be called immediately.**
    - What is happening behind the scenes?
        1. Email address is validated.
        2. Check if email already exists. If not, create a user.
        3. Make an `ImagePost` model entry and store the images locally.
        4. Call the Mask R-CNN API and run prediction on the `top_img`. If this fails, delete the entry.
        5. Store the results of Mask R-CNN in a `PredictedImagePost` entry.
- `/api/update`
    - Request type: `PUT`
    - Request body: (*`post_id`, *`packager`, `materials`, *`score`)
    - Response body: indicates success or failure of the request.
    - Description: This **must** be called immediately after the `score` is calculated with a request body like above. `materials` is dependent on how successful GV is, therefore, it is not a required parameter for this call (but it is highly suggested you put some GV output in the request). If this call were to fail, the post made with `/api/upload` will be deleted.
    - What is happening behind the scenes?
        1. First check if the returned `post_id` from `/api/upload` is exists in the `PredictedImagePost` model. If so, return that instance.
        2. Check if `packager` already exists, if not create a new packager.
        3. Update the `score` in the database with the newly calculated `score` using incremental average method. Update `packager`, `materials`, `score` fields in the entry corresponding to `post_id`.
- `/api/display_feed`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/display_feed?page=NUMBER`
    - Request body: ()
    - Response body: Each array element of `results` will look like the following.
        ```json
        {
            "img_post": {
                "id": 1,
                "top_img": "http://localhost:8000/media/top/1/IMG_3.jpg",
                "side_img": "http://localhost:8000/media/side/1/IMG_26.jpg",
                "infer_img": "http://localhost:8000/media/infer/1/IMG_3.jpg",
                "date_posted": "2020-04-30T07:08:06.336221Z"
            },
            "packager": {
                "brand_name": "Amazon",
                "score": 9.41726906526411
            },
            "score": 7.58,
            "materials": "{'responses':[{'logoAnnotations':[{'mid':'/m/045c7b','description':'google','score':0.980325,'boundingPoly':{'vertices':[{'x':12,'y':42},{'x':439,'y':42},{'x':439,'y':285},{'x':12,'y':285}]}}]}]}",
            "outer_size": 40705,
            "inner_size": 18522,
            "item_size": 3454
        }
        ```
    - Paginated: Yes
    - Description: Shows all available posts in the database, ordered from newest to oldest.
- `/api/search_packager_posts`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/search_packager_post?packager=PACKAGER_NAME?&page=NUMBER`
    - Request body: ()
    - Response body: Would look similar to `/api/display_feed`'s response.
    - Paginated: Yes
    - Description: Shows posts based on `PACKAGER_NAME`, ordered from newest to oldest.
        - Note: `PACKAGER_NAME` must be <a href = "https://www.w3schools.com/tags/ref_urlencode.asp" target="_blank">URL encoded</a> when making the request.
- `/api/search_user_posts`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/search_user_post?email=USER_EMAIL?&page=NUMBER`
    - Request body: ()
    - Response body: Would look similar to `/api/display_feed`'s response.
    - Paginated: Yes
    - Description: Shows posts based on `USER_EMAIL`, ordered from newest to oldest.
        - Note: `USER_EMAIL` must be <a href = "https://www.w3schools.com/tags/ref_urlencode.asp" target="_blank">URL encoded</a> when making the request.
- `/api/display_all_packagers`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/display_all_packagers`
    - Request body: ()
    - Response body: 
        ```json
        {
            "count": 40,
            "next": "http://localhost:8000/api/display_all_packagers?page=2",
            "previous": null,
            "results": [
                {
                    "brand_name": "Alibaba",
                    "score": 9.719938231376535
                },
                {
                    "brand_name": "Amazon",
                    "score": 8.28061327367672
                },
                {
                    "brand_name": "BHLDN",
                    "score": 8.70324039065559
                },
                {
                    "brand_name": "Brooklinen",
                    "score": 9.316997629971663
                },
                {
                    "brand_name": "Costco",
                    "score": 7.590275548346984
                },
                {
                    "brand_name": "Cuyana",
                    "score": 9.634930018553689
                }
                .
                .
                .
            ]
        }
        ```
    - Paginated: Yes
    - Description: Returns all packagers in alphabetical ordering.
- `/api/best_five`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/best_five`
    - Request body: ()
    - Response body: 
        ```json
        [
            {
                "brand_name": "Forever 21",
                "score": 9.943878380327225
            },
            {
                "brand_name": "Louis Vuitton",
                "score": 9.878421489547112
            },
            {
                "brand_name": "J.Crew",
                "score": 9.829957780492606
            },
            {
                "brand_name": "Jumia",
                "score": 9.679675411069166
            },
            {
                "brand_name": "BHLDN",
                "score": 9.531866984077077
            }
        ]
        ```
    - Paginated: Yes
    - Description: Returns the top five best retailers.
- `/api/worst_five`
    - Request type: `GET`
    - URL: `http://localhost:8000/api/worst_five`
    - Request body: ()
    - Response body: 
        ```json
        [
            {
                "brand_name": "Amazon",
                "score": 5.177583157728733
            },
            {
                "brand_name": "Sony",
                "score": 5.206787633369038
            },
            {
                "brand_name": "Prada",
                "score": 5.34022484848443
            },
            {
                "brand_name": "Zappos",
                "score": 5.509269308893511
            },
            {
                "brand_name": "Kors",
                "score": 5.612308312625131
            }
        ] 
        ```
    - Paginated: Yes
    - Description: Returns the top five worst retailers.

---
# Other Information:
- `localhost:8000` can be replaced with `pointlesspackaging.space` if accessing the cloud server.
- Accessing the admin page: `http://localhost:8000/admin` and login as a superuser to have control.
- Can use POSTMAN to make calls to the API as no authentication is needed.
- Example of fully paginated response for `/api/display_feed?page=1`:
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "img_post": {
                    "id": 1,
                    "top_img": "http://localhost:8000/media/top/1/IMG_3.jpg",
                    "side_img": "http://localhost:8000/media/side/1/IMG_26.jpg",
                    "infer_img": "http://localhost:8000/media/infer/1/IMG_3.jpg",
                    "date_posted": "2020-04-30T07:08:06.336221Z"
                },
                "packager": {
                    "brand_name": "Amazon",
                    "score": 9.41726906526411
                },
                "score": 7.58,
                "materials": "{'responses':[{'logoAnnotations':[{'mid':'/m/045c7b','description':'google','score':0.980325,'boundingPoly':{'vertices':[{'x':12,'y':42},{'x':439,'y':42},{'x':439,'y':285},{'x':12,'y':285}]}}]}]}",
                "outer_size": 40705,
                "inner_size": 18522,
                "item_size": 3454
            },
            {
                "img_post": {
                    "id": 2,
                    "top_img": "http://localhost:8000/media/top/1/IMG_23_r1PfAgy.jpg",
                    "side_img": "http://localhost:8000/media/side/1/IMG_23_LqYcfPY.jpg",
                    "infer_img": "http://localhost:8000/media/infer/1/IMG_23_f9tmg18.jpg",
                    "date_posted": "2020-04-30T07:15:33.802592Z"
                },
                "packager": {
                    "brand_name": "eBay",
                    "score": 6.775900552394034
                },
                "score": 6.45,
                "materials": "",
                "outer_size": 35678,
                "inner_size": 19834,
                "item_size": 2954
            }
        ]
    }
    ```

## Warnings:
- Do not mess around with the `accounts` app migration unless you know what you are doing.
- Feel free to overwrite the `requirements.txt` to fit your computer dependency. But do not push it to master. The version that is available is tailored to be compatible Ubuntu 18.04 (which is also what our server runs on).

## Credits:
- (For code used in M-RCNN inference part of this app) https://github.com/bendangnuksung/mrcnn_serving_ready
- (Used this to learn the DJANGO Rest Framework) https://github.com/mitchtabian/CodingWithMitchBlog-REST-API

## Some sources:
- https://docs.djangoproject.com/en/3.0/
- (Making DB queries) https://docs.djangoproject.com/en/3.0/topics/db/queries/
- https://www.django-rest-framework.org/
- https://www.youtube.com/playlist?list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV
- (What is ORM?) https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a