#!/usr/bin/env bash

cd ~/python-getting-started
cp ~/ds-production/source/scripts/echo.py echo.py
echo 'flask' >> requirements.txt
echo "web: gunicorn echo:app" > Procfile

heroku local
