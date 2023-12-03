# RPI Backup:

### QbitTorrent:
Default safe path: `/mnt/extdisk/downloads/`

Bypass authentication for clients in whitelisted IP subnets: 
```
192.168.0.109/32
192.168.0.105/32
192.168.0.104/32
192.168.0.96/28
```

### General:

Crontab -e:
```
@reboot sleep 60 && /home/pi/Durgeshs-pub/bash_script.sh > /home/pi/cronjob_logs/reboot_cronjob.txt 2>&1
*/6 * * * * python3 /home/pi/Durgeshs-pub/cronjob.py > /home/pi/cronjob_logs/cronjob.txt 2>&1

#Update PiHole's gravity block list everyday
@daily root    PATH="$PATH:/usr/local/bin/" pihole updateGravity >/var/log/pihole_updateGravity.log || cat /var/log/pih>

#Start the qbittorrent web UI
@reboot sleep 120 && qbittorrent-nox > /home/pi/cronjob_logs/qbittorrent-log.txt 2>&1
```

