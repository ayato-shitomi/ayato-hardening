pip install flask
cd webapp
sudo systemctl stop http-flask.service
sudo cp ./http-flask.service /etc/systemd/system/
sudo systemctl enable http-flask.service
sudo systemctl restart http-flask.service
sudo systemctl status http-flask.service
