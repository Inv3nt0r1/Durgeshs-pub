#!/bin/bash
. /home/pi/.bashrc
echo "Script loaded at"+date
sudo mount /dev/sda1 /mnt/ExtDiskNas
sudo mount /dev/sda2 /mnt/NextCloudDriveMountPoint
echo "Disks mounted"
python /home/pi/Durgeshs-pub/script.py &
echo "Python program started, sleeping for 30 seconds"
sleep 30
cd /home/pi/Durgeshs-pub/

git add .
git commit -m "This commit is automatically done by the script, to change link of reverse proxy tunnel"
git pull
git push
