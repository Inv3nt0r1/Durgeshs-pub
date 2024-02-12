#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade
sudo apt autoremove


sudo apt install apache2 -y
sudo apt install lsb-release -y
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
sudo apt update

sudo apt install php8.3 php8.3-gd php8.3-sqlite3 php8.3-curl php8.3-zip php8.3-xml php8.3-mbstring php8.3-mysql php8.3-bz2 php8.3-intl php8.3-smbclient php8.3-imap php8.3-gmp php8.3-bcmath libapache2-mod-php8.3 -y

sudo service apache2 restart

sudo apt install mariadb-server -y

