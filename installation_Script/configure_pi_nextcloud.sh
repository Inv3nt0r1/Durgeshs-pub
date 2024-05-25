#!/bin/bash

#Update all libraries and packages
sudo apt update
sudo apt upgrade -y
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade
sudo apt autoremove

#install apache and other required packages for hosting our nextcloud app
sudo apt install apache2 -y
sudo apt install lsb-release -y
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
sudo apt update
sudo apt install php8.3 php8.3-gd php8.3-sqlite3 php8.3-curl php8.3-zip php8.3-xml php8.3-mbstring php8.3-mysql php8.3-bz2 php8.3-intl php8.3-smbclient php8.3-imap php8.3-gmp php8.3-bcmath libapache2-mod-php8.3 -y

#Restart Apache to load latest changes
sudo service apache2 restart

#Install SQL Server mariaDB
sudo apt install mariadb-server -y

#Install Expect for sql installation automation
sudo apt-get install expect -y

SECURE_MYSQL=$(expect -c "
	set timeout 5
	spawn sudo mysql_secure_installation

	expect \"Enter current password for root (enter for none):\"
	send \"\r\"

	expect \"Switch to unix_socket authentication\"
	send \"y\r\"

	expect \"Change the root password?\"
	send \"n\r\"

	expect \"Remove anonymous users?\"
	send \"y\r\"

	expect \"Disallow root login remotely?\"
	send \"y\r\"

	expect \"Remove test database and access to it?\"
	send \"y\r\"

	expect \"Reload privilege tables now?\"
	send \"y\r\"

	expect eof
")

echo "$SECURE_MYSQL"

#Remove expect since we don't need it anymore
sudo apt-get remove expect -y
sudo apt autoremove -y

#Create the nextcloud database and user
# ATTENTION: KINDLY UPDATE THE PASSWORD IN THIS SQL FILE: create_db_nextcloud.sql
sudo mysql -u root "-p\r" < create_db_nextcloud.sql

#open www folder
cd /var/www/

#download latest nextcloud binaries
sudo wget https://download.nextcloud.com/server/releases/latest.tar.bz2

#extract the archive
sudo tar -xvf latest.tar.bz2

#create a data directory for nextcloud to operate in for initial setup
sudo mkdir -p /var/www/nextcloud/data

#give correct permissions for this folder
sudo chown -R www-data:www-data /var/www/nextcloud/
sudo chmod 750 /var/www/nextcloud/data

#-------------Configuring Apache for NextCloud---------------
cd /etc/apache2/sites-available

#Create a configuration file nextcloud and configure it to handle nextcloud under /nextcloud path
cat <<EOF > nextcloud.conf
Alias /nextcloud "/var/www/nextcloud/"

<Directory /var/www/nextcloud/>
  Require all granted
  AllowOverride All
  Options FollowSymLinks MultiViews

  <IfModule mod_dav.c>
    Dav off
  </IfModule>

</Directory>
EOF

#make use of the configuration file created above
sudo a2ensite nextcloud.conf

#Restart Apache2 to force it to read in the updated configuration file
sudo systemctl reload apache2

#Follow next steps from this website: https://pimylifeup.com/raspberry-pi-nextcloud-server/#nextcloud-initial-setup
