#!/usr/bin/env bash
#Set up web server for web_static deployment

#install nginx if it doesn't already exist
sudo install -y nginx

#create directories
sudo mkdir -p /data/web_static/releases/test/

#Simple HTML file to test the configuration
html="<html>
	<head>
		<title>Test File</title>
	</head>
	<body>
		<h1>Test Successful!</h1>
	</body>
</html>"

echo "$html" | sudo tee /data/web_static/releases/test/index.html

#create symbolic link. DELETE and RECREATE link if it already exist
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give folder ownership ubuntu to user and group
chown -R ubuntu:ubuntu /data/

#update nginx to serve the content in the new dir to hbnb_static
config="#serve content in dir\n\tlocation \/hbnb_static {\n\talias \/data\/web_static\/current;\n}\n"

sudo sed -i "/# deny access to .htaccess files, if Apache's document root/i$config" /etc/nginx/sites-available/default

#start nginx if it is newly installed
sudo service nginx start

#Restart nginx
sudo service nginx restart
