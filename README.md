# direwatch
Display direwolf/APRS/packet information on small/adafruit TFT display




Craig Lamparter KM6LYW,  2021, MIT Licnese

This will tail a direwolf log file and display callsigns on an
adafruit st7789 tft display (https://www.adafruit.com/product/4484).
Follow the instructions here to get the driver/library loaded:

https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup

Current configuration is for the 240x240 st7789 unit.

Do not install the kernel module/framebuffer.

GPIO pins 12 (DCD) and 16 (TX) are monitored and light green/red icons
respectively.  Configure these gpio pins in direwolf.


Installation on raspbian/buster for short-attentions span programmers like me:
```
sudo apt-get install python3-pip   # python >= 3.6 required
sudo pip3 install adafruit-circuitpython-rgb-display
sudo pip3 install pyinotify
sudo apt-get install python3-dev python3-rpi.gpio
vi /boot/config.txt  # uncomment following line: "dtparam=spi=on"
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py   ## this gets the digitalio python module
```
