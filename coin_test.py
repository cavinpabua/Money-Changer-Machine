import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

def coin_callback(channel):
    if GPIO.input(channel) != 0:
        print("Coin detected!", channel)

GPIO.add_event_detect(4, GPIO.FALLING, callback=coin_callback)

while True:
    time.sleep(1)
