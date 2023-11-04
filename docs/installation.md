# Getting started

## Pre-requisites

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8 or above with pip](https://www.python.org/downloads/)
- [Make](https://www.gnu.org/software/make/)
- [Preferably running an Ubuntu based OS](https://www.ubuntu.com/download/desktop)

## Installation

Download the installer.zip file from one of the releases, you can find the releases page [here](https://github.com/Evanlab02/ShoppingListApp/releases).

Once you have unzipped the zip file, you should now have a directory called 'ShoppingApp'. Within this directory there is a download directory, you should move into that directory through the terminal. Something like the following:

```bash
cd ShoppingApp/download
```

## Download installer dependencies

The download script is a python file, so you will need a working version of python and some dependencies. You can install the dependencies by running the following command:

```bash
pip install -r requirements.txt
```

## Download sub-releases

Once you have done all the above you should be able to run the download script with the following command:

```bash
python download.py
```

This should download a bunch of zip files into the directory. Once this is done you can move on to the next step.

## Install the app

Now that you have downloaded all the releases, you can install the app. You can do this by running the following command:

```bash
make install
```

This will unzip all the files into the required directories, ensuring a smooth setup for you.

## Here comes some conifguration

There will now be a few files in the ShoppingApp directory, so lets take a step back there. You can cd back to the ShoppingApp directory by running the following command:

```bash
cd ..
```

Now with a file editor of your choice, open the 'application.properties' file in the 'app' directory. Find example below with nano:

```bash
nano app/application.properties
```

You will probably want to change the 'PROD_HOST' value here, I would recommend you just set it to 'localhost' or to whatever domain you would like to use. There are other values you can change here, but these can require changes in several files, so I would recommend you leave them as they are.

Now that you have setup your 'application.properties', run the following command to put your changes into effect on the backend:
    
```bash
make sync
```

## More configuration

Now you will need to setup some other values, you can run the setup process for these values with the following command:

```bash
./setup.sh
```

This script will prompt you for everything you need to setup, so just follow the instructions.

## Now you need docker

Cool now you are setup, stick with me for a little bit longer. Ensure you have docker and docker compose installed before continuing. If you do not have these installed, you can find the installation instructions [here](https://docs.docker.com/install/) and [here](https://docs.docker.com/compose/install/).

## Create static files

You need to generate the static files that will be hosted by the web server. You can do this by running the following command:

```bash
make static
```

## Almost there

Please note you also need port 80, 5050, 5432 and 8000 to be available on your machine. If you are familiar with docker, you can change the ports used in the compose file however be careful not to change the exposed container ports as this will break things.

You can now get the server running where you will need to do some final configuration. You can start the server by running the following command:

```bash
make up
```

## Final configuration

You now need to run some commands in your backend container, the container name will be something along the lines of "-shopping-django-app-" with words and numbers appended to the start and finish of it. In this container you need to run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Now you should be able to access the app

You should now be able to access the app at the domain you set in the 'application.properties' file. You can access the admin panel at the '/admin' endpoint. You can login with the superuser you created in the previous step.

Please be careful of deleting your docker volumes as this will delete all your data if you delete these containers volume. This is where this postgres data is being stored, if you delete it you will have to re-do the final configuration step.

## Shutting down the server

You can shut down the server by running the following command:

```bash
make down
```

## Updating the app

Find the update documentation [here](update.md).
