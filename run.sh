#!/bin/bash
# Defines the config file and entry-point to the app
gunicorn --config  gunicorn.conf.py 'wsgi:create_app()'