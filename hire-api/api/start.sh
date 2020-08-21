#!/bin/bash

echo Applying Migrations...
python manage.py migrate

echo Collecting Staticfiles...
python manage.py collectstatic

echo Running Server...
gunicorn -c gunicorn.conf api.wsgi

