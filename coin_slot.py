import RPi.GPIO as GPIO
import time
# Set up GPIO pin
coin_pin = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define pulse callback function
pulse_count = 0
last_time = 0
def count_pulses(channel):
    global pulse_count, last_time
    curr_time = time.time()
    if curr_time - last_time > 0.05:  # Ignore pulses less than 50ms apart
        pulse_count += 1
        last_time = curr_time
    # pulse_count += 1
    # print(pulse_count)
    print(pulse_count)

# Add interrupt to GPIO pin
GPIO.add_event_detect(coin_pin, GPIO.FALLING, callback=count_pulses)

# Main loop
while True:
    # Wait for user to press "s" key
    if input() == "s":
        # Stop pulse detection and calculate number of coins
        GPIO.remove_event_detect(coin_pin)
        num_coins = pulse_count
        pulse_count = 0
        
        # Dispense coins (replace with your own code for controlling coin hopper)
        print("Dispensing %d coins..." % num_coins)
        
        # Reset GPIO pin for pulse detection
        GPIO.add_event_detect(coin_pin, GPIO.FALLING, callback=count_pulses)
