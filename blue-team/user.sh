for i in {1..11} ; do sudo useradd -m "user${i}"; done
for i in {1..10} ; do echo "user${i}:user${i}" | sudo chpasswd ; done
echo "user11:pass" | sudo chpasswd
sudo useradd dev
echo "dev:devpass123" | sudo chpasswd

cat /etc/passwd | grep -v False | grep -v no | grep -v false
