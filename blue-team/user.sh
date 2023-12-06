for i in {1..11} ; do sudo useradd -m "user${i}"; done
sudo useradd dev
sudo useradd hardening

for i in {1..10} ; do echo "user${i}:user${i}" | sudo chpasswd ; done
echo "root:root" | sudo chpasswd
echo "dev:devpass123" | sudo chpasswd
echo "user11:pass" | sudo chpasswd
echo "hardening:hardening" | sudo chpasswd

for i in {1..10} ; do sudo usermod -aG sudo user${i} | sudo chpasswd ; done
sudo usermod -aG sudo user11
sudo usermod -aG sudo dev
sudo usermod -aG sudo hardening

cat /etc/passwd | grep -v False | grep -v no | grep -v false
