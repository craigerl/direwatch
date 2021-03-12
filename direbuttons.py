#!/usr/bin/python3
import RPi.GPIO as GPIO
import subprocess
from time import sleep

# GPIO buttons, pi tft uses logical 23 and 24 gpio pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)

 
def button_callback_24(number):
    print("Button ",   number,  "  pressed.")

    if number == 24:                                       # start digipeater
        try:
            cmd = "sudo systemctl status digipeater"
            status = "active"
            cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            status = "inactive"
        print("status:", status, ":")
        if status == "inactive":
            print("___stop tnc")
            try:
                cmd = "sudo systemctl stop tnc"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
            print("___stop winlinkrms")
            try:
                cmd = "sudo systemctl stop winnkrms"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
            print("___start digipeater")
            try:
                cmd = "sudo systemctl start digipeater"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
    return(0)

def button_callback_23(number):
    print("Button ",   number,  "  pressed.")

    if number == 23:                                        # start TNC/igate
        try:
            cmd = "sudo systemctl status tnc"
            status = "active"
            cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            status = "inactive"
        if status == "inactive":
            print("___stop digipeater")
            try:
                cmd = "sudo systemctl stop digipeater"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
            print("___stop winlinkrms")
            try:
                cmd = "sudo systemctl stop winnkrms"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
            print("___start tnc")
            try:
                cmd = "sudo systemctl start tnc"
                cmd_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except:
                pass
    return(0)

GPIO.add_event_detect(24,GPIO.FALLING,callback=button_callback_24,bouncetime=300)
GPIO.add_event_detect(23,GPIO.FALLING,callback=button_callback_23,bouncetime=300)

print("sleeping forever...")
# better way of doing nothing without an import?
while True:
   sleep(10000000)
