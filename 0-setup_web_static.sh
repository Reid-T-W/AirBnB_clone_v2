#!/usr/bin/env bash
# Sets up a server for the deployment if web_static
# Installing nginx if not installed
if ! hash nginx 2>/dev/null
then
	apt-get -y update
	apt-get -y install nginx
	ufw allow 'Nginx HTTP'
fi
# Creating the folder /data/ if it doesn't already exist
DIR="/data/"
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi

# Creating the folder /data/web_static/ if it doesn’t already exist
DIR="/data/web_static/"
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi
# Creating the folder /data/web_static/releases/ if it doesn’t already exist
DIR="/data/web_static/releases/"
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi

# Creating the folder /data/web_static/shared/ if it doesn’t already exist
DIR="/data/web_static/shared/"
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
DIR="/data/web_static/releases/test/"
if [ ! -d "$DIR" ]; then
	mkdir $DIR
fi

# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content)
FILE="/data/web_static/releases/test/index.html"
if [ ! -f "$FILE" ]; then
	touch $FILE
	echo "some simple content" > $FILE
fi
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
LINK="/data/web_static/current"
SOURCE_DIR="/data/web_static/releases/test/"
if  [ -L $LINK ];
then
	rm $LINK
	ln -s $SOURCE_DIR $LINK
else
	ln -s $SOURCE_DIR $LINK
fi	
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
DIR="/data/"
chown -R ubuntu:ubuntu $DIR
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
# old_string="try_files \$uri \$uri\/ =404;\n	}"
# final_string="${old_string}\n\n	location \/hbnb_static {\n		alias \/data\/web_static\/current\/;\n	}"
# sed -i "N; s/$old_string/$final_string/g" /etc/nginx/sites-available/default
final_string="location \/hbnb_static {\n		alias \/data\/web_static\/current\/;\n	}"
sed -i "63i\	$final_string" /etc/nginx/sites-available/default
# Restaring nginx
service nginx restart
