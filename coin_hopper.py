import RPi.GPIO as GPIO
import time 
# Set up the GPIO pin
hopper_pin = 18 # ANALOG 1 PIN
GPIO.setmode(GPIO.BCM)
GPIO.setup(hopper_pin, GPIO.IN)
coin_count = 0

# Loop forever, checking for changes in the GPIO pin state
prev_input = GPIO.input(hopper_pin)
while True:
    input_state = GPIO.input(hopper_pin)
    if input_state != prev_input:
        if input_state == GPIO.LOW:
            print("GPIO pin went from high to low")
            coin_count += 1
        else:
            print("GPIO pin went from low to high")
        print("Count:", coin_count)
        prev_input = input_state
        time.sleep(0.05)