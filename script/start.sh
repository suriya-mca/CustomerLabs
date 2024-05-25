#!/bin/sh

python manage.py makemigrations
python manage.py migrate

gunicorn core.wsgi:application -c /etc/gunicorn/gunicorn.conf.py