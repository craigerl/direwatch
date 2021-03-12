#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT Licnese

This will tail a direwolf log file and display callsigns on an
adafruit st7789 tft display (https://www.adafruit.com/product/4484).  
Follow the instructions here to get the driver/library loaded:

https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup

Current configuration is for the 240x240 st7789 unit.

Do not install the kernel module/framebuffer.

GPIO pins 12 (PTT) and 16 (DCD) are monitored and light green/red icons respectively.
Configure these gpio pins in direwolf.


Installation on raspbian/buster for short-attentions span programmers like me:

sudo apt-get install python3-pip   # python >= 3.6 required
sudo pip3 install adafruit-circuitpython-rgb-display
sudo pip3 install pyinotify
sudo apt-get install python3-dev python3-rpi.gpio
vi /boot/config.txt  # uncomment following line: "dtparam=spi=on"
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py   ## this gets the digitalio python module


Much code taken from ladyada for her great work driving these devices,
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""

import argparse
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import re
import adafruit_rgb_display.st7789 as st7789  
import pyinotify
#import RPi.GPIO as GPIO
import threading
import signal
import os

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
#reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()


# Use one and only one of these screen definitions:

## half height adafruit screen 1.1" (240x135), two buttons
#disp = st7789.ST7789(
#    board.SPI(),
#    cs=cs_pin,
#    dc=dc_pin,
#    rst=reset_pin,
#    baudrate=BAUDRATE,
#    width=135,
#    height=240,
#    x_offset=53,
#    y_offset=40,
#    rotation=270,
#)

# full height adafruit screen 1.3" (240x240), two buttons
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
#    rst=reset_pin,
    baudrate=BAUDRATE,
    height=240,
    y_offset=80 
)

# don't write to display concurrently with thread
display_lock = threading.Lock()

# Create image and drawing object
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(image)

# define some constants to help with graphics layout
padding = 4 
title_bar_height = 34


def signal_handler(signal, frame):
   print("Got ", signal, " exiting.")
   draw.rectangle((0, 0, width, height), outline=0, fill=(30,30,30))
   with display_lock:
       disp.image(image)
   #sys.exit(0)  # thread ignores this
   os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)



def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--log", required=True, help="Direwolf log file location")
    ap.add_argument("-f", "--fontsize", required=False, help="Font size for callsigns")
    ap.add_argument("-t", "--title_text", required=False, help="Text displayed in title bar")
    args = vars(ap.parse_args())
    return args

args = parse_arguments()
logfile = args["log"]
if args["fontsize"]:
   fontsize = int(args["fontsize"])
else:
   fontsize = 20   
if args["title_text"]:
   title_text = args["title_text"]
else:
   title_text = "Direwatch"


## GPIO buttons, pi tft uses logical 23 and 24 gpio pins
## I moved this to direbuttons.py so we don't kill/restart ourselves
## This is an example if you want to use the buttons here.
## Uncomment the GPIO import at the top of this file if you want buttons.
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23,GPIO.IN)
#GPIO.setup(24,GPIO.IN)
#
#def button_callback(number):
#    print("Button ",   number,  "  pressed.")
#    if number == 23:
#        pass
#    if number == 24:
#        pass
#
#GPIO.add_event_detect(23,GPIO.FALLING,callback=button_callback,bouncetime=300) 
#GPIO.add_event_detect(24,GPIO.FALLING,callback=button_callback,bouncetime=300)
       

# Bluetooth LED connection check 

def bluetooth_connection_poll_thread():
    bt_status = 0
    while True:
        cmd = "hcitool con | wc -l"
        connection_count = subprocess.check_output(cmd, shell=True).decode("utf-8")
        if int(connection_count) > 1:
            if bt_status == 0:
                bt_status = 1
                print("BT ON")
                bticon = Image.open('bt.small.on.png')   
                #image.paste(bticon, (148,6), bticon)
                image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)
                with display_lock:
                    disp.image(image)
        else:
            if bt_status == 1:
                bt_status = 0  
                bticon = Image.open('bt.small.off.png')   
                image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)
                #image.paste(bticon, (148,6), bticon)
                with display_lock:
                    disp.image(image)
        time.sleep(2)

bluetooth_thread = threading.Thread(target=bluetooth_connection_poll_thread, name="btwatch")
bluetooth_thread.start()


# Status LEDs thread

def handle_changeG(cb):
   with open('/sys/class/gpio/gpio16/value', 'r') as f:          ## GREEN
      status = f.read(1)
      if status == '0':
         draw.ellipse(( width - title_bar_height               , padding,       width - padding * 2,                  title_bar_height - padding), fill=(0,80,0,0))
      else:
         draw.ellipse(( width - title_bar_height               , padding,       width - padding * 2,                  title_bar_height - padding), fill=(0,200,0,0))
      with display_lock:
         disp.image(image)
   f.close

def handle_changeR(cb):
   with open('/sys/class/gpio/gpio12/value', 'r') as f:          ## RED
      status = f.read(1)
      if status == '0':
         draw.ellipse(( width - title_bar_height * 2           , padding,    width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(80,0,0,0))
      else:
         draw.ellipse(( width - title_bar_height * 2           , padding,    width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(200,0,0,0))
         pass
      with display_lock:
         disp.image(image)
   f.close

def null_function(junk):  # default callback prints tons of debugging info
   return()

# Instanciate a new WatchManager (will be used to store watches).
wmG = pyinotify.WatchManager()
wmR = pyinotify.WatchManager()

# Associate this WatchManager with a Notifier
notifierG = pyinotify.Notifier(wmG, default_proc_fun=null_function)
notifierR = pyinotify.Notifier(wmR, default_proc_fun=null_function)

# Watch both gpio pins for change
wmG.add_watch('/sys/class/gpio/gpio16/value', pyinotify.IN_MODIFY)
wmR.add_watch('/sys/class/gpio/gpio12/value', pyinotify.IN_MODIFY)

#run led watch threads in background
watch_threadG = threading.Thread(target=notifierG.loop, name="led-watcherG", kwargs=dict(callback=handle_changeG))
watch_threadR = threading.Thread(target=notifierR.loop, name="led-watcherR", kwargs=dict(callback=handle_changeR))
watch_threadG.start()
watch_threadR.start()


# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
line_height = font.getsize("ABCJQ")[1] - 1          # tallest callsign, with dangling J/Q tails
max_line_width = font.getsize("KN6MUC-15")[0] - 1   # longest callsign i can think of in pixels
max_cols = width // max_line_width
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw our logo
w,h = font.getsize(title_text)
draw.text(   (padding * 3  ,  height // 2 - h) ,   title_text, font=font_huge,   fill="#99AA99")
time.sleep(5)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# draw the header bar
draw.rectangle((0, 0, width, title_bar_height), fill=(30, 30, 30))
draw.text((padding, padding), title_text, font=font_big, fill="#99AA99")

bticon = Image.open('bt.small.off.png')
image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)

# Green LED
draw.ellipse(( width - title_bar_height               , padding,       width - padding * 2,                  title_bar_height - padding), fill=(0,80,0,0))

# Red LED
draw.ellipse(( width - title_bar_height * 2           , padding,    width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(80,0,0,0))

# position cursor in -1 slot, as the first thing the loop does is increment slot
y = padding + title_bar_height - font.getsize("ABCJQ")[1]  

with display_lock:
    disp.image(image)

call = "null"
x = padding
max_lines  = ( height - title_bar_height - padding )  //   line_height 
max_cols = ( width // max_line_width )
line_count = 0
col_count = 0 

# tail and block on the log file
f = subprocess.Popen(['tail','-F','/run/direwolf.log'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

while True:
    line = f.stdout.readline().decode("utf-8", errors="ignore")
    search = re.search("^\[\d\.\d\] ([a-zA-Z0-9-]*)", line)

    if search is not None:
       lastcall = call
       call = search.group(1)
    else:
       continue

    if call == lastcall:   # blink duplicates
       time.sleep(0.5)
       draw.text((x, y), call, font=font, fill="#000000")
       with display_lock:
           disp.image(image)
       time.sleep(0.1)
       draw.text((x, y), call, font=font, fill="#AAAAAA")
       with display_lock:
           disp.image(image)
    else:
       y += line_height
       if line_count == max_lines:       # about to write off bottom edge of screen
           col_count += 1
           x = col_count * max_line_width  
           y = padding + title_bar_height
           line_count = 0
       if col_count == max_cols:         # about to write off right edge of screen
           x = padding 
           y = padding + title_bar_height
           draw.rectangle((0, title_bar_height + 1, width, height), outline=0, fill=0) # erase lines
           line_count = 0
           col_count = 0
           time.sleep(2.0)
       draw.text((x, y), call, font=font, fill="#AAAAAA")
       line_count += 1
       with display_lock:
           disp.image(image)


exit(0)

