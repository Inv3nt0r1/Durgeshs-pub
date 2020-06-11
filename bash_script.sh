
#!/bin/bash
python3 /home/pi/Durgeshs-pub/script.py &
sleep 60
cd /home/pi/Durgeshs-pub/
git add .
git commit -m "This commit is automatically done by the script, to change link of reverse proxy tunnel"
git push
