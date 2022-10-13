# twitchchatviewer

## Description

A website written in Django and JavaScript, designed to view messages from Twitch chat logged by [twitchlogger](https://github.com/retrontology/twitchlogger)

## Installation
**Note**:I've only included an example apache2 configuration file so I will only cover deployment to that webserver. However this can be deployed to any webserver that supports wsgi. This guide also assumes you have already installed and configured the system dependencies required for Django to run on apache2.

1. Install the webserver
   a. Copy the `src` directory to `/var/www/webserver` (or wherever you want to serve your files from).
   b. Enter the directory you just copied ot, edit the `420-twitchchatviewer.conf` configuration file and define `WEBSERVERROOT` as the directory you copied to in the previous step.
   c. Initiate the db by running the commands: 
   ```
   sudo python manage.py makemigrations
   sudo python manage.py migrate
   ```
3. Create the virtual environment
   a. Create a virtual environment by changing the directory to the webserver root and running the command 
   ```
   sudo python3 -m venv .
   ```
   b. Activate the newly created virtual environment by running the command
   ```
   source bin/activate
   ```
   c. Install the required dependencies by running the command
   ```
   sudo pip install -r requirements.txt
   ```
   d. Exit the virtual environment
4. Install the static files
   a. Enter the webserver root you set up in the first step
   b. Edit `webserver/settings.py` and change `STATIC_ROOT` to the directory you want to serve your static files from. It's set to `/var/www/twitchchatviewer` by default.
   c. Deploy the static files by running the command 
   ```
   sudo python3 manage.py collectstatic
   ```
   d. Edit the `420-twitchchatviewer.conf` configuration file and define `STATICROOT` as the directory you set as the static root in the previous step.
5. Install the apache2 configuration
   a. Move the `420-twitchchatviewer.conf` configuration file you've been editing to `/etc/apache2/sites-available/`
   b. Enable the site with the command:
   ```
   sudo a2ensite 420-twitchchatviewer.conf
   ```
   c. Reload apache2 with the command:
   ```
   sudo systemctl reload apache2
   ```