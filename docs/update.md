# Updating

Updating is much simpler than installing, you can find the instructions for updating below.

## Shut down your server

You will need to shut down your server before updating, you can do this by running the following command:

```bash
make down
```

## Uninstall all old files

You will need to uninstall all old files, you can do this by running the following command:

```bash
make uninstall
```

## Use the download script

Change directory into the download directory:

```bash
cd download
```

And then run the download script with python:

```bash
python download.py
```

This will download all the required files into the download directory.

## Install the app

Now that you have downloaded all the releases, you can install the app. You can do this by running the following command:

```bash
make install
```

You will be prompted if you would like to reinstall the Makefile, you can say yes to this.

## Sync the backend

Change directory out of the downloads folder:

```bash
cd ..
```

Now that you have installed the app, you will need to sync the backend with your existing settings. You can do this by running the following command:

```bash
make sync
```

## Generate the static files

You will need to generate the static files for the frontend, you can do this by running the following command:

```bash
make static
```

## You can start your server again

Now that you have updated the app, you can start your server again. You can do this by running the following command:

```bash
make up
```
