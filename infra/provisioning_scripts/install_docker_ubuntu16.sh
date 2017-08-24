# Provision Docker Ubuntu 16
# It installs docker and configure current user to being able to acces docker without sudo

#Docker user
USER=$(whoami)

#Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo usermod -aG docker ${USER}
id -nG