import RPi.GPIO as GPIO
import time
from PyQt5 import QtWidgets, uic
import sys
import time
import os
os.environ["DISPLAY"] = ":0"

GPIO.setmode(GPIO.BCM)

# Define pins
coin_pin = 2
bill_acceptor_pin = 5
bill_inhibitor_pin = 6
relay_1_pin = 17
relay_2_pin = 18
relay_3_pin = 27
relay_4_pin = 22
relay_5_pin = 23
ir_sensor_1_pin = 24
ir_sensor_2_pin = 25
ir_sensor_3_pin = 8
ir_sensor_4_pin = 7
ir_sensor_5_pin = 12
try:
    GPIO.setup(coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(bill_acceptor_pin, GPIO.IN)
    GPIO.setup(bill_inhibitor_pin, GPIO.IN)
    GPIO.setup(relay_1_pin, GPIO.OUT)
    GPIO.setup(relay_2_pin, GPIO.OUT)
    GPIO.setup(relay_3_pin, GPIO.OUT)
    GPIO.setup(relay_4_pin, GPIO.OUT)
    GPIO.setup(relay_5_pin, GPIO.OUT)
    GPIO.setup(ir_sensor_1_pin, GPIO.IN)
    GPIO.setup(ir_sensor_2_pin, GPIO.IN)
    GPIO.setup(ir_sensor_3_pin, GPIO.IN)
    GPIO.setup(ir_sensor_4_pin, GPIO.IN)
    GPIO.setup(ir_sensor_5_pin, GPIO.IN)

    prev_input_1 = GPIO.input(ir_sensor_1_pin)
    prev_input_2 = GPIO.input(ir_sensor_2_pin)
    prev_input_3 = GPIO.input(ir_sensor_3_pin)
    prev_input_4 = GPIO.input(ir_sensor_4_pin)  
    prev_input_5 = GPIO.input(ir_sensor_5_pin)

    GPIO.output(relay_1_pin, GPIO.LOW)
    GPIO.output(relay_2_pin, GPIO.LOW)
    GPIO.output(relay_3_pin, GPIO.LOW)
    GPIO.output(relay_4_pin, GPIO.LOW)
    GPIO.output(relay_5_pin, GPIO.LOW)

except:
    GPIO.cleanup()
    exit()


coin_count = 0
last_time = 0
DELAY_TIME = 0.5
credit_flag = False
credit_timer = 0



app = QtWidgets.QApplication([])
window = uic.loadUi("main.ui")
bills_window = uic.loadUi("to_bills.ui")
coins_window = uic.loadUi("to_coins.ui")



# Get reference to LCD number widget
lcd_coin_counter = window.lcd_coin_counter

# Interrupt callback for credit signal
def credit_callback(channel):
    global credit_flag
    global credit_timer

    # Set credit flag and timer
    credit_flag = True
    credit_timer = time.time()

# Interrupt callback for Inhibitor+ signal
def inhibitor_callback(channel):
    global credit_flag
    global credit_timer
    global coin_count

    # Check if credit flag is set and delay time has passed
    if credit_flag and (time.time() - credit_timer) >= DELAY_TIME:
        # Add credit and reset credit flag
        coin_count += 1
        credit_flag = False


def pulse_detected(channel):
    global coin_count
    global last_time
    global lcd_coin_counter
    curr_time = time.time()
    if curr_time - last_time > 0.05:  # Ignore pulses less than 50ms apart
        coin_count += 1
        last_time = curr_time

    lcd_coin_counter.display(coin_count)





GPIO.add_event_detect(coin_pin, GPIO.FALLING, callback=pulse_detected)
GPIO.add_event_detect(bill_acceptor_pin, GPIO.RISING, callback=credit_callback)
# Set up interrupt detection for Inhibitor+ signal
GPIO.add_event_detect(bill_inhibitor_pin, GPIO.RISING, callback=inhibitor_callback)


# Define button click handlers
def to_bills_clicked():
    global window, bills_window
     # check if coin count is greater than 0
    if coin_count == 0:
        return
    def to_100_bills_clicked():
        global coin_count
        global lcd_coin_counter, bills_window, coins_window, window
        bills_to_dispense = [100, 50, 20]
        remaining_coins = dispense(coin_count, bills_to_dispense)
        coin_count = remaining_coins
        lcd_coin_counter.display(coin_count)
        if remaining_coins > 0:
            remaining_coins_to_dispense = [5, 1] if remaining_coins < 5 else [1]
            dispense(remaining_coins, remaining_coins_to_dispense)
            coin_count = 0
            lcd_coin_counter.display(coin_count)
        try:
            bills_window.hide()
            coins_window.hide()
            window.show()
        except:
            window.show()
    def to_50_bills_clicked():
        global coin_count
        global lcd_coin_counter, bills_window, coins_window, window
        bills_to_dispense = [50, 20]
        remaining_coins = dispense(coin_count, bills_to_dispense)
        coin_count = remaining_coins
        lcd_coin_counter.display(coin_count)
        if remaining_coins > 0:
            remaining_coins_to_dispense = [5, 1] if remaining_coins < 5 else [1]
            dispense(remaining_coins, remaining_coins_to_dispense)
            coin_count = 0
            lcd_coin_counter.display(coin_count)
        try:
            bills_window.hide()
            coins_window.hide()
            window.show()
        except:
            window.show()
    def to_20_bills_clicked():
        global coin_count
        global lcd_coin_counter, bills_window, coins_window, window
        bills_to_dispense = [20]
        remaining_coins = dispense(coin_count, bills_to_dispense)
        coin_count = remaining_coins
        lcd_coin_counter.display(coin_count)
        if remaining_coins > 0:
            remaining_coins_to_dispense = [5, 1] if remaining_coins < 5 else [1]
            dispense(remaining_coins, remaining_coins_to_dispense)
            coin_count = 0
            lcd_coin_counter.display(coin_count)
        try:
            bills_window.hide()
            coins_window.hide()
            window.show()
        except:
            window.show()
    bills_window.to_100_bills.clicked.connect(to_100_bills_clicked)
    bills_window.to_50_bills.clicked.connect(to_50_bills_clicked)
    bills_window.to_20_bills.clicked.connect(to_20_bills_clicked)
    window.hide()
    bills_window.show()


def to_coins_clicked():
    global window, coins_window
     # check if coin count is greater than 0
    if coin_count == 0:
        return
    def to_5_coins_clicked():
        global coin_count
        global lcd_coin_counter, bills_window, coins_window, window
        remaining_coins = dispense(coin_count, [5, 1])
        coin_count = 0
        lcd_coin_counter.display(coin_count)
        if remaining_coins > 0:
            dispense(remaining_coins, [1])
        try:
            bills_window.hide()
            coins_window.hide()
            window.show()
        except:
            window.show()

    def to_1_coins_clicked():
        global coin_count
        global lcd_coin_counter, bills_window, coins_window, window
        dispense(coin_count, [1])
        coin_count = 0
        lcd_coin_counter.display(coin_count)
        try:
            bills_window.hide()
            coins_window.hide()
            window.show()
        except:
            window.show()
    coins_window.to_5_coins.clicked.connect(to_5_coins_clicked)
    coins_window.to_1_coins.clicked.connect(to_1_coins_clicked)
    window.hide()
    coins_window.show()

def dispense(coins, denominations):
    global window, coins_window, bills_window
    for denomination in denominations:
        print("Number of {} bills: {}".format(denomination, coins // denomination))
        count = coins // denomination
        operate_dispenser(count, denomination)
        coins = coins % denomination
    # show main.ui
    
    return coins


def operate_dispenser(count, denomination):
    global prev_input_1, prev_input_2, prev_input_3, prev_input_4, prev_input_5
    dispenser_count = 0
    
    if denomination == 100:
        # turn on relay 1
        GPIO.output(relay_1_pin, GPIO.HIGH)
        # loop and add to dispenser count, until count is reached, with delay to allow for IR sensor to detect and avoid false positives or spamming
        while dispenser_count < count:
            input_state_1 = GPIO.input(ir_sensor_1_pin)
            if input_state_1 != prev_input_1:
                if input_state_1 == GPIO.LOW:
                    dispenser_count += 1
                    if dispenser_count >= count:
                        print("dispenser count reached")
                        GPIO.output(relay_1_pin, GPIO.LOW)
                prev_input_1 = input_state_1
                time.sleep(0.5)
    elif denomination == 50:
        # turn on relay 2
        GPIO.output(relay_2_pin, GPIO.HIGH)
        # loop and add to dispenser count, until count is reached, with delay to allow for IR sensor to detect and avoid false positives or spamming
        while dispenser_count < count:
            input_state_2 = GPIO.input(ir_sensor_2_pin)
            if input_state_2 != prev_input_2:
                if GPIO.input(ir_sensor_2_pin):
                    dispenser_count += 1
                    if dispenser_count >= count:
                        print("dispenser count reached")
                        GPIO.output(relay_2_pin, GPIO.LOW)
                prev_input_2 = input_state_2
                time.sleep(0.5)
        # turn off relay 2
    elif denomination == 20:
        # turn on relay 3
        GPIO.output(relay_3_pin, GPIO.HIGH)
        # loop and add to dispenser count, until count is reached, with delay to allow for IR sensor to detect and avoid false positives or spamming
        while dispenser_count < count:
            input_state_3 = GPIO.input(ir_sensor_3_pin)
            if input_state_3 != prev_input_3:
                if GPIO.input(ir_sensor_3_pin):
                    dispenser_count += 1

                    if dispenser_count >= count:
                        print("dispenser count reached")
                        GPIO.output(relay_3_pin, GPIO.LOW)
                prev_input_3 = input_state_3
                time.sleep(0.5)
    elif denomination == 5:
        # turn on relay 4
        print("Turning on relay 4")
        GPIO.output(relay_4_pin, GPIO.HIGH)
        # loop and add to dispenser count, until count is reached, with delay to allow for IR sensor to detect and avoid false positives or spamming
        while dispenser_count < count:
            input_state_4 = GPIO.input(ir_sensor_4_pin)
            if input_state_4 != prev_input_4:
                print("changes detected in IR sensor 4")
                # if GPIO.input(ir_sensor_4_pin):
                dispenser_count += 1
                if dispenser_count >= count:
                    GPIO.output(relay_4_pin, GPIO.LOW)
                    print("dispenser count reached")

                prev_input_4 = input_state_4
                time.sleep(0.3)
        # turn off relay 4
        GPIO.output(relay_4_pin, GPIO.LOW)
    elif denomination == 1:
        # turn on relay 5
        GPIO.output(relay_5_pin, GPIO.HIGH)
        # loop and add to dispenser count, until count is reached, with delay to allow for IR sensor to detect and avoid false positives or spamming
        while dispenser_count < count:
            input_state_5 = GPIO.input(ir_sensor_5_pin)
            if input_state_5 != prev_input_5:
                if GPIO.input(ir_sensor_5_pin):
                    dispenser_count += 1
                    if dispenser_count >= count:
                        print("dispenser count reached")
                        GPIO.output(relay_5_pin, GPIO.LOW)
                prev_input_5 = input_state_5
                time.sleep(0.5)
    return count



# Connect button click handlers
window.to_bills.clicked.connect(to_bills_clicked)
window.to_coins.clicked.connect(to_coins_clicked)

window.show()
sys.exit(app.exec())

