#!/bin/bash

# Railway start script
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn mpls.wsgi:application
