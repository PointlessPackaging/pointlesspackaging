# HOW TO SETUP AND RUN THE API FOR THE FIRST TIME


1. Open up the terminal in this directory and `cd server`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
    - So you can have control over the admin page.
    - This will prompt you for email, username (just put your first name), password confirm password.
    - The password can be something small like "193". However, if you do have small somthing small like that, then you will have to 'override' when Django asks if you want to.
5. `python manage.py runserver`

If you have already made the migrations, skip step 2 and 3.
If you have already made a superuser, skip step 4.

The API should be running!

Goto admin page: http://localhost:8000/admin/ and login to have control.

Use POSTMAN to make UNAUTHENTICATED requests:

1. http://localhost:8000/api/create_hello - append to body `name` and `msg` field and make a `POST` request.
2. http://localhost:8000/api/get_hello - make a `GET` request, this will query everything in the database table `hello_rest`.

Use POSTMAN to make AUTHENTICATED requests:

0. Register a user by making a `POST` request. 
    - enter http://localhost:8000/accounts/register into the URL field. 
    - Click on 'Body' below the URL field. The `key`s are `email`, `username`, `password`, `password2`. Enter `value`s of your choice. And press 'Send'.
    - You will recive a JSON that looks like this:
        ```
        {
        "response": "Account Registered.",
        "email": "yoyo@abc.com",
        "username": "Yeeet",
        "token": "7a39fe5f41f840a2302c8adaf5f8ac8309886aa5"
        }
        ```
    - Save that token.
1. `POST` with http://localhost:8000/api/upload - with 'Body' keys and values.
    - The `key`s are: `packager`, **`top_img`, **`side_img`
    - ** make sure you select 'File' in the Key drop down meny for these.
    - Click on Headers
        - Key: type in `Authorization`
        - Value: type in `token 7a39fe5f41f840a2302c8adaf5f8ac8309886aa5`
    - Click on send. The image should be uploaded.
2. `GET` with http://localhost:8000/api/display_feed?page=1 to display all uploaded images. No authentication required for this. That means, you don't have to put your tokens in the header.
3. The tokens for each user can also be found here:
    - http://localhost:8000/admin/authtoken/token/

## Credit:
- (For code used in M-RCNN inference part of this app) https://github.com/bendangnuksung/mrcnn_serving_ready

## Some sources:
- https://docs.djangoproject.com/en/3.0/
- (Making DB queries) https://docs.djangoproject.com/en/3.0/topics/db/queries/
- https://www.django-rest-framework.org/

- https://www.youtube.com/playlist?list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV
- https://github.com/mitchtabian/CodingWithMitchBlog-REST-API

- (What is ORM?) https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a