#!/bin/bash

# Installs the dependencies for the GreenHope project
# Written 4/28/2024
# Owen Johnson, based on script by Trevor Ladner (of ENGR 16X)

echo
echo "Performing Installation Script"
echo

echo "you are logged in as: " $USER
echo

nc -z -w 5 8.8.4.4 53  >/dev/null 2>&1
online=$?
if [ $online -eq 0 ]; then
    echo "Internet connection found"
else
    echo "NO INTERNET CONNECTION DETECTED - ABORTING (press any key to exit)"
    read temp
    exit
fi

#echo "ensuring Pi is up to date"
#sudo apt update
#sudo apt upgrade

runv1=0
runv2=0
while [ $runv1 -eq 0 ] && [ $runv2 -eq 0 ]; do
    read -p "Are you running as the Hub or a Module (h/m) " hm
    case $hm in
        [Hh]* ) runv1=1; break;;
        [Mm]* ) runv2=1; break;;
        * ) echo "Please answer h for Hub or m for Module.";;
    esac
done

echo "installing CAN hat dependencies"
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz 
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install

cd
sudo apt-get install wiringpi
#For Raspberry Pi systems after May 2019 (earlier than that can be executed without), an upgrade may be required:
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
# Run gpio -v and version 2.52 will appear, if it doesn't it means there was an installation error

# Bullseye branch system using the following command:
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
gpio -v

wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master
sudo make install
#Raspberry Pi 5 
sudo apt install python3-rpi-lgpio

sudo apt-get install python3-serial
sudo apt-get install python3-can

sudo echo "dtparam=spi=on" >> /boot/config.txt
sudo echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" >> /boot/config.txt

if [ $runv1 -eq 1 ]; then #running as the hub
		echo "Installing dependencies for the hub"
		sudo pip install -r hub/requirements.txt

		echo "installing mariadb-server"
		sudo apt install mariadb-server
		echo "follow prompts for MySQL below (most secure install requires 'y' to all y/n prompts). Be sure to write down the password you create in this process: "
		sudo mysql_secure_installation
		
		echo "installing Grafana"
		sudo mkdir -p /etc/apt/keyrings/
		wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
		echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
		sudo /bin/systemctl enable grafana-server
		sudo /bin/systemctl start grafana-server
else #running as the module
		echo "Installing dependencies for the module"
		sudo pip install -r module/requirements.txt
fi



echo 
echo 
echo
echo "PLEASE REBOOT FOR CHANGES TO TAKE EFFECT"
echo "(press any button to exit)"
echo " ______"
echo "| |__| |"
echo "|  ()  |"
echo "|______|"
read temp
