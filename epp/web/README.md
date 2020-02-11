1. Setting up your virtual environment
    - run `python3 -m venv venv3`
    - run `source venv3/bin/activate`

2. Install linkers
    - run `pip3 install -r requirements.txt -U`
    - check what installed, run `pip3 freeze`

3. Run website
    - run `python manage.py runserver` within your *virtual environment* in the directory containing **manage.py** 
    
Others

1. Add new app
    - `python manage.py startapp  <app_name>`
    - `python manage.py makemigrations`
    - add new class in models.py
    - `python manage.py migrate`

2. Create supersuer 
    - `python manage.py createsuperuser`
    
3. Create object through shell
    - `python manage.py shell`
    - `from uploader.models import Uploader`
    - `Uploader.objects.all()`
    - `Uploader.objects.create(title='Hello user!')`

4. Port-In-Used Error
    - `sudo lsof -t -i tcp:8000 | xargs kill -9`


