#REQUESITOS ORACLE CLOUD
##API KEY GOOGLE DRIVE (DESKTOP APP)##
cd C:\Users\mcama\Documents\Cursos\Oracle\Plex
ID CLIENTE: 795843089909-50uhj3lraalhirm7as89smudvq14jumi.apps.googleusercontent.com
SECRETO DE CLIENTE: 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
Team Drive: 0AE-pnfKeOiINUk9PVA
sudo chown -R $USER:$USER /path/to/directory
#Enlaces de interes
https://www.youtube.com/watch?v=CNRTXPKI3AU
https://www.youtube.com/watch?v=mnDYJ2ZpdxU&t=344s
https://cloudbit.es/index.php?resources/como-montar-un-servidor-de-plex-con-google-drive-y-plex-drive.1/
https://www.reddit.com/r/PleX/comments/2fo868/guide_how_to_set_up_a_cloud_plex_server_for_as/
https://www.how2shout.com/how-to/how-to-install-plex-media-server-on-amazon-lightsail.html

#1 Habilitar puertos en UBUNTU
ssh -i "ssh-key-2021-12-04.key" -L 127.0.0.1:53682:127.0.0.1:53682 ubuntu@150.230.165.158
sudo apt install nmap -y
sudo nmap -sS -sV -p 80 -Pn 150.230.165.158
sudo iptables -L INPUT
sudo vim /etc/iptables/rules.v4
sudo iptables-restore < /etc/iptables/rules.v4

#2 PLEX
sudo wget https://downloads.plex.tv/plex-media-server-new/1.28.0.5999-97678ded3/debian/plexmediaserver_1.28.0.5999-97678ded3_arm64.deb
sudo dpkg -i package.deb
sudo systemctl start plexmediaserver
sudo systemctl enable plexmediaserver
sudo systemctl status plexmediaserver

#3 RCLONE
sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 53682 -j ACCEPT
sudo wget https://github.com/rclone/rclone/releases/download/v1.46/rclone-v1.46-linux-arm64.deb
sudo dpkg -i package.deb
rclone --version
rclone config
http://127.0.0.1:53682/auth

#4 Mount rclone
sudo vim /etc/fuse.conf #Habilitar el enable
mkdir /home/plexcloud
rclone mount --allow-other --allow-non-empty -v mauriciodrive: /home/plexcloud &

#4 Tunnel Local Host Plex
ssh -i "ssh-key-2021-12-04.key" -L 127.0.0.1:32400:127.0.0.1:32400 ubuntu@150.230.165.158
sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 32400 -j ACCEPT
http://127.0.0.1:32400/web

