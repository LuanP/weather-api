#!/bin/sh

NAME="weather-api"
DJANGODIR=/app
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=app.settings
DJANGO_WSGI_MODULE=app.wsgi

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

cd $DJANGODIR

./manage.py migrate

gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind 0.0.0.0:80 \
  --log-level debug \
  --timeout 6000 \
  --log-file - \
  --keep-alive 5 \
  --access-logfile -
