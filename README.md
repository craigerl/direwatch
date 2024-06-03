# direwatch
by KM6LYW

Display direwolf/APRS/packet information on small/adafruit TFT display (and/or png file).

```
direwatch.py  --log "/root/direwolf.log" --title_text "APRS digi" --font 20  
```
Demonstration:  https://m.youtube.com/watch?v=W_V4wE3F5GM

Newer demonstration (with symbols):  https://www.youtube.com/watch?v=NJ_IJNU7NA0&t=7s

Craig Lamparter KM6LYW,  2021, MIT Licnese

This will tail a direwolf log file and display callsigns on an
adafruit st7789 tft display (https://www.adafruit.com/product/4484).
Follow the instructions here to get the driver/library loaded:

https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup

Three screens are supported ST7789 240x240, ST7789 240x135, ILI9341 240x360.

Current configuration is for the 240x240 st7789 unit.

Uncomment the screen section for your particular screen around line 100.

Do not install the kernel module/framebuffer.

GPIO pins 12 (DCD) and 16 (TX) are monitored and light green/red icons
respectively.  Configure these gpio pins in direwolf.

For Pi5, use digibuttons.gpiod.py, for other Pi's use digibuttons.rpigpio.py or digibuttons.gpiozero .


![Ygate with Direwatch](http://craiger.org/ygatescreen.png)


Installation on raspbian/buster for short-attentions span programmers like me:
```
Installation on raspbian/bullseye for short-attentions span programmers like me:
  sudo apt-get install python3-pip   # python >= 3.6 required
  sudo apt-get install gpiozero
  sudo pip3 install adafruit-circuitpython-rgb-display
  sudo pip3 install pyinotify
  sudo apt-get install python3-dev python3-rpi.gpio
  vi /boot/config.txt  # uncomment following line: "dtparam=spi=on"
  sudo pip3 install --upgrade adafruit-python-shell
  wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
  sudo python3 raspi-blinka.py   ## this gets the digitalio python module
  sudo pip install aprslib     ## so we can parse ax.25 packets

Installation on raspbian/bookworm
   sudo rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
   sudo pip3 install Adafruit-Blinka
   sudo pip3 install python3-numpy
   sudo pip3 install adafruit-circuitpython-rgb-display
   sudo pip3 install aprslib
   vi /boot/config.txt  # uncomment following line: "dtparam=spi=on"

```

Special thanks to hessu for the svg aprs symbols https://github.com/hessu/aprs-symbols
