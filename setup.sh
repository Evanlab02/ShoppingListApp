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

echo Saving your environment settings to .env file...
touch .env
echo DJANGO_DATABASE_USER="$dbuser" >> .env
echo DJANGO_DATABASE_NAME="$dbname" >> .env
echo PGADMIN_DEFAULT_EMAIL="$pguser" >> .env
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