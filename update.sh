echo ""
echo ------------------ BACKEND UPDATE ------------------
echo "Removing previous backend installation..."
rm -rf backend
rm -rf backend.zip
echo "Please specify the backend version here for installation (Example: 0.11.0):"
read version
echo ----------------------------------------------------
echo ""

echo ""
echo ------------------- FRONTEND UPDATE -------------------
echo "Removing previous frontend installation..."
rm -rf shoppingapp-fe.zip
rm -rf dist
echo "Please specify the frontend version here for installation (Example: 0.8.0):"
read feversion
echo -------------------------------------------------------
echo ""

echo ""
echo ------------------- SERVER UPDATE -------------------
echo "Please always check if the newest server version is backwards compatible"
echo ""
echo "If you are many versions behind, please be sure to check all versions between"
echo "the current and your chosen one are backwards compatible"
echo ""
echo "If they are not, you will need to redownload your chosen release"
echo "If you use the update script, it will break your installation"
echo "if it is not backwards compatible"
echo ""
echo "NOTE: Server update will only be fully implemented in 0.7.0"
echo "For now, please update the server manually until then"
echo ""
echo "Please specify the server version here for installation (Example: 0.5.0):"
read serverversion
echo -------------------------------------------------------

echo ""
echo ------------------- DOWNLOADING BACKEND -------------------
echo "Downloading Backend..."
wget https://github.com/Evanlab02/ShoppingListApp-BE/archive/refs/tags/v$version.zip
mv v$version.zip backend.zip
echo -----------------------------------------------------------
echo ""

echo ""
echo ------------------- UNZIPPING BACKEND -------------------
echo "Unzipping Backend..."
unzip backend.zip -d backend
echo ---------------------------------------------------------
echo ""

echo ""
echo ------------------- RESTRUCTURING BACKEND -------------------
echo "Restructuring Backend..."
shopt -s dotglob
mv backend/ShoppingListApp-BE-$version/* backend/
echo -------------------------------------------------------------
echo ""

echo ""
echo ------------------- DOWNLOADING FRONTEND -------------------
echo "Downloading Frontend..."
wget https://github.com/Evanlab02/ShoppingListApp-FE/releases/download/v$feversion/shoppingapp-fe.zip
echo -------------------------------------------------------------
echo ""

echo ""
echo ------------------- UNZIPPING FRONTEND -------------------
echo "Unzipping Frontend..."
unzip shoppingapp-fe.zip
echo ----------------------------------------------------------
echo ""

echo ""
echo ------------------- ENV UPDATE -------------------
echo Updating .env file...
head -n -3 .env > .env.tmp
mv .env.tmp .env
echo BACKEND_VERSION="$version" >> .env
echo FRONTEND_VERSION="$feversion" >> .env
echo SERVER_VERSION="$serverversion" >> .env
echo --------------------------------------------------
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