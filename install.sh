echo ""
echo ------------------- STARTING INSTALLATION -------------------
echo Cleaning previous installation if it exists
rm -rf backend
rm -rf backend.zip
rm -rf .env
rm -rf shoppingapp-fe.zip
rm -rf dist
echo -------------------------------------------------------------
echo ""

echo ""
echo ------------------- NOTE -------------------
echo Please ensure you have docker and docker compose installed 
echo before installing this application. If you have docker desktop
echo installed, please ensure it is open and running.
echo ""
echo "This script will try and run docker from the command line without sudo."
echo "If this will not work, please refer to the README for the manual installation"
echo ""
read -p "Press enter to continue"
echo ---------------------------------------------

echo ""
echo ------------------- DOWNLOADING BACKEND -------------------
echo "Please specify the backend version here for installation (Example: 0.11.0):"
read version
echo ""
echo "Downloading Backend..."
echo ""
wget https://github.com/Evanlab02/ShoppingListApp-BE/archive/refs/tags/v$version.zip
mv v$version.zip backend.zip
echo -----------------------------------------------------------
echo ""

echo ""
echo ------------------- UNZIPPING BACKEND -------------------
echo "Unzipping Backend..."
echo ""
unzip backend.zip -d backend
echo ---------------------------------------------------------
echo ""

echo ""
echo ------------------- RESTRUCTURING BACKEND -------------------
echo "Restructuring Backend..."
shopt -s dotglob
mv backend/ShoppingListApp-BE-$version/* backend/
rm -rf backend/shoppingapp/settings/local_settings.py
rm -rf backend/shoppingapp/settings/dev_settings.py
rm -rf backend/shoppingapp/settings/test_settings.py
echo -------------------------------------------------------------
echo ""

echo ""
echo ------------------- DOWNLOADING FRONTEND -------------------
echo "Please specify the frontend version here for installation (Example: 0.8.0):"
read feversion
echo ""
echo "Downloading Frontend..."
echo ""
wget https://github.com/Evanlab02/ShoppingListApp-FE/releases/download/v$feversion/shoppingapp-fe.zip
echo -------------------------------------------------------------
echo ""

echo ""
echo ------------------- UNZIPPING FRONTEND -------------------
echo "Unzipping Frontend..."
echo ""
unzip shoppingapp-fe.zip
echo ----------------------------------------------------------
echo ""

echo ""
echo ------------------- ENV SETUP -------------------
echo Please enter a username for the database
read dbuser
echo ""
echo Please enter a name for the database
read dbname
echo ""
echo Please enter a email for the pgadmin
read pguser
echo ""
serverversion=`cat version.txt`

echo Saving your environment settings to .env file...
touch .env
echo DJANGO_DATABASE_USER="$dbuser" >> .env
echo DJANGO_DATABASE_NAME="$dbname" >> .env
echo PGADMIN_DEFAULT_EMAIL="$pguser" >> .env
echo BACKEND_VERSION="$version" >> .env
echo FRONTEND_VERSION="$feversion" >> .env
echo SERVER_VERSION="$serverversion" >> .env
echo -------------------------------------------------
echo ""

echo ""
echo ------------------- CREDENTIALS -------------------
mkdir -p secrets
echo Please enter a password for the database
read dbpass
# Copy dbpass to secrets/dbpass.txt file
echo $dbpass > secrets/dbpass.txt
echo ""
echo Please enter a secret key for the Django app
read secretkey
# Copy secretkey to secrets/djkey.txt file
echo $secretkey > secrets/djkey.txt
echo ""
echo Please enter a admin password for PGADMIN
read pgpass
# Copy pgpass to secrets/pgadmin.txt file
echo $pgpass > secrets/pgadmin.txt
echo ---------------------------------------------------
echo ""

echo ""
echo ----------------- SYNC -----------------
echo "Updating application properties file with current one"
cp application.properties backend/application.properties
echo ----------------------------------------
echo ""

echo ""
echo ------------------- DOCKER -------------------
echo "Building Docker Images..."
echo ""
make build
echo ""
echo "Pulling Docker Images..."
docker pull dpage/pgadmin4:7.8
docker pull postgres:alpine3.18
echo ----------------------------------------------
echo ""

echo ------------------- CLEANING UP -------------------
echo Cleaning up installation files...
rm -rf backend.zip
rm -rf shoppingapp-fe.zip
rm -rf backend/
rm -rf dist/
rm -rf static/
echo ---------------------------------------------------
echo ""

echo ""
echo ------------------- INSTALLATION COMPLETE -------------------
echo Please ensure you have docker and docker compose installed before trying to run this application
echo ""
echo Run the application with 'make up'
echo ""
echo Stop the application with 'make down'
echo ""
echo Uninstall the application from docker with 'make uninstall', note this will wipe out all data and is not recoverable
echo -------------------------------------------------------------
echo ""