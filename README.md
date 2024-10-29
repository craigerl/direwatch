# direwatch
by KM6LYW

Display direwolf/APRS/packet information on small/adafruit TFT display (and/or png file).

```
example: direwatch.py  --log "/root/direwolf.log" --title_text "APRS digi" --font 20

usage: direwatch.py [-h] -l LOG [-f FONTSIZE] [-t TITLE_TEXT] [-o] [-y LAT] [-x LON] [-s SAVEFILE] [-d screentype]

options:
  -h, --help            show this help message and exit
  -l LOG, --log LOG     Direwolf log file location
  -f FONTSIZE, --fontsize FONTSIZE
                        Font size for callsigns
  -t TITLE_TEXT, --title_text TITLE_TEXT
                        Text displayed in title bar
  -o, --one             Show one station at a time full screen
  -y LAT, --lat LAT     Your Latitude -123.4567
  -x LON, --lon LON     Your Longitude 23.4567
  -s SAVEFILE, --savefile SAVEFILE
                        Save screen updates to png file
  -d DISPLAY, --display DISPLAY
                        st7789, ili9341, or ili9486


```

Newer demonstration (with symbols):  https://www.youtube.com/watch?v=NJ_IJNU7NA0&t=7s

Craig Lamparter KM6LYW,  2021, MIT Licnese

This will tail a direwolf log file and display callsigns on a small tft display:

  https://www.adafruit.com/product/4484   (st7789)
  https://www.adafruit.com/product/2423   (ili9341) 
  https://www.amazon.com/Resistive-Screen-IPS-Resolution-Controller/dp/B07V9WW96D  (ili9486)

Three screens are supported st7789 240x240, ili9341 240x360, ili9486 320x480

Default configuration is for the 240x240 st7789 screen.  

Specify screen type with "-d" option.
   st7789
   ili9341
   ili9486

Do not install the kernel module/framebuffer.

Red/Green indicators use direwolf's log file, be sure to add "-d o" to
the direwolf command line for this feature to work.


![Ygate with Direwatch](http://craiger.org/direwatch.png)


Shopping list for a PiZero2W SDR APRS receive-only igate

- $18 pizero 2w with headers https://www.adafruit.com/product/6008
- $4  USB adapter cable      https://amazon.com/UGREEN-Adapter-Samsung-Controller-Android/dp/B00N9S9Z0G
- $31 RTL-SDR                https://amazon.com/RTL-SDR-Blog-RTL2832U-Software-Defined/dp/B0CD745394
- $32 Antenna                https://www.ebay.com/itm/321819895073?_nkw=n9tax&itmmeta=01J6YZSM7069JH3ZSYV3X1XS0Q
- $14 Display                https://www.amazon.com/DIYmall-Display-240x240-Raspberry-ST7789/dp/B08F9VD2GZ



Installation on Raspberry Pi OS Bookworm, including optional rtl-sdr receiver:
```
sudo apt-get update
sudo apt-get install direwolf rtl-sdr git python3-pip fonts-dejavu python3-pil python3-pyinotify python3-numpy python3-libgpiod python3-lgpio
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
PBEACON sendto=IG compress=1 delay=00:15 every=30:00 symbol="igate" overlay=X lat=40.911 long=-122.935 comment="Direwatch Rx-only igate"
AGWPORT 8000
KISSPORT 8001
ADEVICE null
""""""""""""""""""""""

cd direwatch
rtl_fm  -s 22050 -g 49 -f 144.39M 2> /dev/null | direwolf -d o -t 0 -r 22050  -   > direwolf.log &
./direwatch.py -o  -l direwolf.log -t "APRS"

```

Special thanks to hessu for the svg aprs symbols https://github.com/hessu/aprs-symbols
