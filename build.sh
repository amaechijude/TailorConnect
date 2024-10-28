#!/bin/bash
python3 -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
# python3 manage.py makemigrations
# python3 migrate
# python3 manage.py collectstatic --noinput