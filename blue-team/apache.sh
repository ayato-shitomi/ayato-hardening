sudo apt install apache2 -y
sudo systemctl enable apache2
sudo mkdir /var/www/html
sudo cp ./webapp/README.md /var/www/html
sudo cp ./ports.conf /etc/apache2/ports.conf
sudo systemctl restart apache2
sudo systemctl status apache2
