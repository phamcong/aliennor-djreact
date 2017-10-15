install.md
# Django React web dev

## Install Backend Django
### Create a virtualenv and install Django and DRF
```
$ virtualenv env
$ source env/bin/activate
$ pip install django djangorestframework django-filter
$ pip freeze > requirements.txt
```

### Start Django project and Django app
```
$ django-admin startproject backend
$ cd backend
$ django-admin startapp api
```

### Set a user, create database and runserver to test
```
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Install Frontend React
### Install frontend with create-react-app
```
$ npm install -g create-react-app
$ create-react-app frontend
$ cd frontend
$ npm run eject
```

### Install some additional dependencies
```
$ npm install --save-dev babel-preset-es2015 babel-preset-stage-3
$ npm install --save redux redux-logger redux-persist react-redux
$ npm install --save axios react-router-dom lodash
````

## Refs:
[Creating websites using React and Django REST Framework](https://hackernoon.com/creating-websites-using-react-and-django-rest-framework-b14c066087c7)
