#!/usr/bin/env bash

sudo yum update
sudo yum install gcc python-setuptools postgresql-devel

sudo easy_install psycopg2

pip install --user django
pip install --user django-heroku
