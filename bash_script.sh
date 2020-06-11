#!/bin/bash
. /home/pi/.bashrc

file="/tmp/test.txt"
echo "Adding first line" > $file
echo "Adding first line replaced" > $file
echo "Appending second line " >> $file
echo "Appending third line" >> $file
cat $file
python3 /home/pi/Durgeshs-pub/script.py &
file="/tmp/test1.txt"
echo "Adding first line" > $file
echo "Adding first line replaced" > $file
echo "Appending second line " >> $file
echo "Appending third line" >> $file
cat $file
sleep 30
cd /home/pi/Durgeshs-pub/
git add .
git commit -m "This commit is automatically done by the script, to change link of reverse proxy tunnel"
git push
