#!/usr/bin/env bash

cd ~
curl -o heroku-linux-x64.tar.gz https://cli-assets.heroku.com/heroku-linux-x64.tar.gz
tar xzf heroku-linux-x64.tar.gz
cd ~/.local/bin/ && ln -s ~/heroku/bin/heroku heroku

sudo yum update
sudo yum -y install glibc.i686

heroku --version
