#!/bin/bash
set -x

# Out of the box, the apt package manager does not have support for repositories running behind HTTPS.
# To work around this, we can install the apt-transport-https package by running the following command.
sudo apt install apt-transport-https lsb-release -y

# Import GPG Signing key of Jellyfin
curl https://repo.jellyfin.org/debian/jellyfin_team.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/jellyfin-archive-keyring.gpg >/dev/null

# Add the Jellyfin Repository to sources.list
echo "deb [signed-by=/usr/share/keyrings/jellyfin-archive-keyring.gpg arch=$( dpkg --print-architecture )] https://repo.jellyfin.org/debian $( lsb_release -c -s ) main" | sudo tee /etc/apt/sources.list.d/jellyfin.list

# Update the packages since we have added the new Jellyfin repo
sudo apt update

# Install Jellyfin
sudo apt install jellyfin

# Follow the further steps as required: https://pimylifeup.com/raspberry-pi-jellyfin/