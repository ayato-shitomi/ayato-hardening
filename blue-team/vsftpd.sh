sudo systemctl stop http-flask.service
sudo apt-get install build-essential
sudo useradd nobody
sudo mkdir /usr/share/empty
cd ./vsftpd-2.3.4-infected
sudo cp vsftpd /usr/local/sbin/vsftpd
sudo cp vsftpd.8 /usr/local/man/man8
sudo cp vsftpd.conf.5 /usr/local/man/man5
sudo cp vsftpd.conf /etc
sudo mkdir /var/ftp/
useradd -d /var/ftp ftp
sudo chown root:root /var/ftp
sudo chmod og-w /var/ftp
sudo cp ./ftpd.service /etc/systemd/system/
sudo systemctl enable ftpd.service
sudo systemctl start ftpd.service
sudo systemctl restart ftpd.service
sudo systemctl status ftpd.service
