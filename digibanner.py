#!/usr/bin/python3

# digibanner.py

"""
Craig Lamparter KM6LYW,  2024, MIT Licnese

This will display a splash screen on an ST7789 or ILI9341 displays.

Usage:

digibanner.py --big="big text on top" --small="small text under that"  --tiny="tiny text at bottom" --graphic="icon.png"

Do not install the kernel module/framebuffer.

Uncomment one of the three display definitions below depending
on your particular monitor.  Default is the small ST7789/240x240 display.

See the top of direwatch.py for installation instructions and dependencies

Much code taken from ladyada for her great work driving these devices,
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""

import argparse
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789  
import adafruit_rgb_display.ili9341 as ili9341 
import os
import subprocess

# Configuration for CS and DC pins (these are PiTFT defaults):
#pin = digitalio.DigitalInOut(board.D4)  # blinkatest
#cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
cs_pin = digitalio.DigitalInOut(board.D4)
#dc_pin = digitalio.DigitalInOut(board.D4)
#reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000   # ST7789
BAUDRATE = 16000000   # ILI9341

# Setup SPI bus using hardware SPI:
spi = board.SPI()


# Use one and only one of these screen definitions:

## half height adafruit screen 1.1" (240x135), two buttons   
## this screen isn't exactly supported any longer
#disp = st7789.ST7789(
#    board.SPI(),
#    cs=cs_pin,
#    dc=dc_pin,
#    baudrate=BAUDRATE,
#    width=135,
#    height=240,
#    x_offset=53,
#    y_offset=40,
#    rotation=270,
#)

## full height adafruit screen 1.3" (240x240), two buttons
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    baudrate=BAUDRATE,
    height=240,
    y_offset=80,
    rotation=180
)

## full height adafruit screen 2.8" (320x240), two buttons
#disp = ili9341.ILI9341(
#    spi,
#    cs=cs_pin,
#    dc=dc_pin,
#    baudrate=BAUDRATE,
#    width=240,
#    height=320,
#    rotation=270
#)



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

def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fontsize", required=False, help="Font size for callsigns")
    ap.add_argument("-b", "--big", required=False, help="large text to display")
    ap.add_argument("-s", "--small", required=False, help="smaller text underneath")
    ap.add_argument("-t", "--tiny", required=False, help="tiny text underneath smaller text")
    ap.add_argument("-i", "--ip", required=False, help="display IP address instead of tiny text")
    ap.add_argument("-g", "--graphic", required=False, help="Display a small image on screen")
    args = vars(ap.parse_args())
    return args

args = parse_arguments()

if args["fontsize"]:
   # 17 puts 11 lines 2 columns
   # 20 puts 9 lines
   # 25 puts 7 lines    
   # 30 puts 6 lines   ** default
   # 34 puts 5 lines, max width
   fontsize = int(args["fontsize"])
   if fontsize > 30:
      print("Look, this display isn't very wide, the maximum font size is 34pts, and you chose " + str(fontsize) + "?")
      print("Setting to 34 instead.")
      fontsize = 34
else:
   fontsize = 30

if args["big"]:
   big = args["big"]
else:
   big = "DigiPi"

if args["small"]:
   small = args["small"]
else:
   small = ""

if args["tiny"]:
   tiny = args["tiny"]
else:
   tiny = ""

if args["ip"]:
   cmd = "hostname -I | cut -d' ' -f1"
   IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
   if ( len(IP) < 5 ):
       IP = "0.0.0.0"
   tiny = IP

if args["graphic"]:
   graphic = args["graphic"]

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
line_height = font.getbbox("ABCJQ")[3] - 1          # tallest callsign, with dangling J/Q tails
font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=(0,0,0), fill="#000000")

if args["graphic"]:
   background = Image.open(args["graphic"])
   image.paste(background, (width - 120, 37), background)

draw.rectangle((0, 0, width, 30), outline=(0,0,0), fill="#333333")
draw.text(   (10  ,  0  ) , "DigiPi", font=font_big, fill="#888888")
draw.text(   (10  ,  height * .28 )                                   , big,   font=font_huge, fill="#888888")
draw.text(   (10  ,  height * .28 + font_big.getbbox("BgJ")[3] + 12 ) , small, font=font_big,  fill="#666666")
draw.text(   (10  ,  height       - font_big.getbbox("BgJ")[3] - 4  ) , tiny,  font=font_tiny, fill="#666666")
disp.image(image)
image.save("/run/direwatch.png") 

exit(0)
