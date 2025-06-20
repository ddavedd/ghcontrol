#! /usr/bin/bash
# Set up a virtual environment because python wants us to
sudo apt-get install build-essential python3-pip python3-dev python3-smbus git
python3 -m venv .gh_control_venv
source .gh_control_venv/bin/activate
sudo .gh_control_venv/bin/pip3 install -U minimalmodbus
sudo .gh_control_venv/bin/pip3 install SM8relind
# Enbale SSH - Login from remote computer for troubleshooting
sudo raspi-config nonint do_ssh 0
# Enable I2C - SM3relind
sudo raspi-conifg nonint do_i2c 0
# Enable 1Wire Thermostats
sudo raspi-config nonint do_onewire 0
# Enable UART - SM3relind
# Only do this if sm3 wont work
sudo raspi-config nonint do_serial_hw 0
# Install sm3relind from git, not available in pip3 yet
git clone https://github.com/SequentMicrosystems/3relind-rpi.git
git clone https://github.com/SequentMicrosystems/8relind-rpi.git
#git clone https://github.com/SequentMicrosystems/8relay-rpi.git
cd ~/3relind-rpi
sudo make install
cd python/3relind/
sudo python3 setup.py install
cd ~/8relind-rpi
sudo make install
#cd python/lib8relind/
#sudo python3 setup.py install
# For arduino connectivity
# sudo usermod -a -G dialout <username> if below doesn't work'
sudo adduser $USER dialout
sudo chmod a+rw /dev/ttyACM0
# To get arduino uno r4 wifi boards to work, need to go to board manager in arduino ide and update
cd ~
git init
git remote add origin https://github.com/ddavedd/ghcontrol.git
git pull origin main
