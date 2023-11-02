echo ""
echo ----------------- UNINSTALL -----------------
echo Removing backend...
rm -rf backend
echo Removing backend installation files...
rm -rf backend.zip
echo Removing frontend...
rm -rf dist
echo Removing frontend installation files...
rm -rf shoppingapp-fe.zip
echo Removing static files...
rm -rf static
echo Removing environment file...
rm -rf .env
echo Removing secrets...
rm -rf secrets
echo ---------------------------------------------
echo ""

echo "----- NOTE -----"
echo "All docker related items will remain on your device."
echo "----------------"

echo COMPLETE
echo ""