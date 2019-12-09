#!/bin/bash

domains=( "arnheim.online" )
rsa_key_size=4096
data_path="./certbot"
email="jhnnsrs@gmail.com" #Adding a valid address is strongly recommended
staging=0 #Set to 1 if you're just testing your setup to avoid hitting request limits

echo "### Preparing directories in $data_path ..."
rm -Rf "$data_path"
mkdir -p "$data_path/www"
mkdir -p "$data_path/conf/live/$domains"


echo "### Creating dummy certificate ..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$path"
docker-compose -f docker-compose.yml -f docker-compose.conf.yml run certbot "\
    openssl req -x509 -nodes -newkey rsa:1024 -days 1\
      -keyout '$path/privkey.pem' \
      -out '$path/fullchain.pem' \
      -subj '/CN=localhost'"


echo "### Downloading recommended HTTPS parameters ..."
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"


