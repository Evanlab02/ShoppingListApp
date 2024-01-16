NOTE: WORK IN PROGRESS

Before jumping into specific files, first thing is to look into the general project structure. Django has its own way of structuring projects which I will cover along with the other file and folders used to create this backend.

## Project structure

With django there is a difference between projects and apps. Apps are the children of the project and together create the full project. Find below a brief example of the backend structure (NOTE: As the backend is not V1 yet, this project structure is how it intended to be structured by the release of V1 but is subject to change)


```markdown-tree
shoppingapp (project)/
authentication (app)/
stores (app)/
items (app)/
lists (app)/
```

While this is the skeleton of the project, there are a lot more folders than just that which will be covered later in more depth.

Next, lets look at the django project folder in more depth. This houses the primary configuration for the project and ties all the apps together.

### Project Structure - Shopping App Django Project

```markdown-tree
shoppingapp
	config
		__init__.py
		asgi.py
		dev_config.py
		local_config.py
		wsgi.py
	schemas
		__init__.py
		shared.py
	settings
		__init__.py
		dev_settings.py
		lite_settings.py
		local_settings.py
		settings.py
	__init__.py
	urls.py
```

This is the structure for the shoppingapp folder (the django project folder). This structure is very unlikely to change.

#### Config folder

Retroactively I realise that 'config' might not have been the best name for this folder. This folder is meant to house different files that will run the asgi or wsgi server with different settings (for different environments).

'Asgi.py' is the entry point for the project when it is running in a production environment.

```markdown-tree
config
	__init__.py
	asgi.py
	dev_config.py 
	local_config.py
	wsgi.py
```

- __asgi.py__ -> ASGI server that will run with the prod settings.
- __dev_config.py__ -> ASGI server that will run with dev settings.
- __local_config.py__ -> ASGI server that will run with local settings.
- __wsgi.py__ -> WSGI server that will run with the prod settings.

#### Schema Folder

Important distinction to make here is that the schema folder in the project folder, is not the same as those we will find in the apps.

For this schema folder, it is primarily for schema's that will be shared across multiple apps or that need to be extended upon in multiple apps.

```markdown-tree
schemas
	__init__.py
	shared.py
```

__shared.py__ -> contains all our shared schema's. Currently this is the only schema file inside the project directory.

#### Settings

This folder contains all our settings/configurations for our app. This is important when it comes to running in different environments as there will be different hosts, ports, passwords, users etc in each.

```markdown-tree
settings
	__init__.py
	dev_settings.py
	lite_settings.py
	local_settings.py
	settings.py
```

- __dev_settings.py__ -> Contains the dev environment settings. This is primarily used when running the backend from the backend repo using docker compose.
- __lite_settings.py__ -> Contains a version of the settings that is oriented around using a SQLite DB instead of Postgres. This is used when running the tests and might even be identical to the local_settings.py (Goes without saying, this should not be used in a production environment)
- __local_settings.py__ -> Contains the local environment settings. This is primarily used when running the backend without a container or running the tests.
- __setttings.py__ -> Contains the production environment settings. Changes to this should be minimal and security here is important.

#### Urls.py

This along with the settings, is where the apps get combined. We add our routers, exception handlers and apps pages here. This along with the __settings.py__ are important files and tie our apps together. Be sure to read more about these files in the docs.

### Project Structure - Django App Structure

We will use the stores app to illustrate our structure, please note there might be some deviations in other apps but they will still follow the base structure and that is all I am attempting to highlight here.

```markdown-tree
stores
	database/
	errors/
	migrations/
	routers/
	schemas/
	services/
	static/
	templates/
	tests/
	__init__.py
	admin.py
	apps.py
	constants.py
	models.py
	urls.py
	views.py
```

The above is the stores app structure and is almost identical to our base app structure. Below I will go through each directory and explain the purpose. I will also explain some files purpose but not all.

