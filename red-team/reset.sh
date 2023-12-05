sshpass -p 'root' scp ../out.zip root@$1:/root
sshpass -p 'root' ssh $1 -l root "cd ~/ && unzip -o out.zip && rm -rf hardening && mv -f ./blue-team ./hardening && cd hardening && ./user.sh && ./vsftpd.sh && ./webapp.sh && ./apache.sh && ./end.sh && cd .. && rm -rf ./hardening/end.sh && rm -rf ./out.zip && echo done"
sshpass -p 'hardening' ssh $1 -l hardening "echo hardening | sudo -S systemctl start http-flask.service & echo hardening | sudo -S userdel test & echo hardening | sudo -S userdel sg & echo hardening | sudo -S  rm /var/www/html/hacked"

# for i in {47.245.32.239,47.245.42.7,47.74.7.149,47.245.58.155,47.245.4.82,47.245.56.27,47.74.45.165,47.91.30.23} ; do ./restart-ftp.sh "${i}"  ; done