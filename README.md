# direwatch
by KM6LYW

Display direwolf/APRS/packet information on small/adafruit TFT display (and/or png file).

```
example: direwatch.py  --log "/root/direwolf.log" --title_text "APRS digi" --font 20

usage: direwatch.py [-h] -l LOG [-f FONTSIZE] [-t TITLE_TEXT] [-o] [-y LAT] [-x LON] [-s SAVEFILE]

options:
  -h, --help            show this help message and exit
  -l LOG, --log LOG     Direwolf or ygate log file location
  -f FONTSIZE, --fontsize FONTSIZE
                        Font size for callsigns
  -t TITLE_TEXT, --title_text TITLE_TEXT
                        Text displayed in title bar
  -o, --one             Show one station at a time full screen
  -y LAT, --lat LAT     Your Latitude -123.4567
  -x LON, --lon LON     Your Longitude 23.4567
  -s SAVEFILE, --savefile SAVEFILE
                        Save screen updates to png file

```

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


Installation on Raspberry Pi OS Bookworm, including optional rtl-sdr receiver:
```
apt-get update
apt-get install direwolf rtl-sdr git adafruit-circuitpython-rgb-display python3-pip fonts-dejavu  python3-pil python3-pyinotify python3-numpy
sudo pip3  install --break-system-packages adafruit-circuitpython-rgb-display
sudo pip3  install --break-system-packages aprslib

git clone https://github.com/craigerl/direwatch.git

sudo nano /boot/firmware/config.txt  # uncomment spi
"""""""""""""""""
dtparam=spi=on
"""""""""""""""""

(reboot)


nano direwolf.conf
""""""""""""""""""""""
MYCALL NOCALL
IGSERVER noam.aprs2.net
IGLOGIN NOCALL 12345
PBEACON sendto=IG compress=1 delay=00:15 every=30:00 symbol="igate" overlay=X lat=39.911 long=-121.935 comment="Direwatch Rx-only igate"
AGWPORT 8000
KISSPORT 8001
ADEVICE null
""""""""""""""""""""""

cd direwatch
rtl_fm  -s 22050 -g 49 -f 144.39M 2> /dev/null | direwolf -t 0 -r 22050  -   > direwolf.log &
./direwatch.py -o  -l direwolf.log -t "APRS"

```

Special thanks to hessu for the svg aprs symbols https://github.com/hessu/aprs-symbols
