#!/usr/bin/env bash

cd ~/python-getting-started

heroku git:remote -a warm-plains-93636
git add .
git commit -m "Test echo service"
git push heroku master

heroku ps:scale web=1
