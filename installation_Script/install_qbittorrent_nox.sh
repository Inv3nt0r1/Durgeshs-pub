#!/bin/bash
set -x

# Upgrade the packages
sudo apt update
sudo apt upgrade -y
sudo apt full-upgrade -y

# Install Qbittorrent headless version
sudo apt-get install qbittorrent-nox -y

# Create a user qbittorrent for the service
sudo useradd -r -m qbittorrent

# Add the pi user to the qbittorrent group
sudo usermod -a -G qbittorrent pi

# Create service file and add necessary details
cd /etc/systemd/system

sudo cat <<EOF > qbittorrent.service
[Unit]
Description=qBittorrent
After=network.target

[Service]
Type=forking
User=qbittorrent
Group=qbittorrent
UMask=002
ExecStart=/usr/bin/qbittorrent-nox -d --webui-port=8998
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Start the qbittorrent service
sudo systemctl start qbittorrent

# Checck the status of qbittorrent service
sudo systemctl status qbittorrent

# Enable qbittorrent service at startup
sudo systemctl enable qbittorrent