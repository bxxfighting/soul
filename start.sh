#!/bin/bash
gunicorn -c gunicorn.py -k gevent soul.wsgi:application
