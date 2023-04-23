import RPi.GPIO as GPIO
import time
from PyQt5 import QtWidgets, uic
import sys
import time
import os
os.environ["DISPLAY"] = ":0"

GPIO.setmode(GPIO.BCM)

# Define pins
coin_pin = 3
bill_acceptor_pin = 9
bill_inhibitor_pin = 10
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
    GPIO.setup(bill_acceptor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(bill_inhibitor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
DELAY_TIME = 0.05
credit_flag = False
credit_timer = 0
COUNT_DELAY = 0.02



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
    print("pumasok sa credit_callback")

    # Set credit flag and timer
    credit_flag = True
    credit_timer = time.time()

# Interrupt callback for Inhibitor+ signal
def inhibitor_callback(channel):
    global credit_flag
    global credit_timer
    global coin_count, lcd_coin_counter
    print("pumasok sa inhibitor_callback")

    # Check if credit flag is set and delay time has passed
    if credit_flag and (time.time() - credit_timer) >= DELAY_TIME:
        # Add credit and reset credit flag
        print("credited!")
        coin_count += 1
        credit_flag = False

        lcd_coin_counter.display(coin_count)


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
GPIO.add_event_detect(bill_acceptor_pin, GPIO.FALLING, callback=credit_callback)
# Set up interrupt detection for Inhibitor+ signal
GPIO.add_event_detect(bill_inhibitor_pin, GPIO.FALLING, callback=inhibitor_callback)


def to_100_bills_clicked():
    global coin_count, lcd_coin_counter, bills_window, coins_window, window
    # disable to_100_bills, to_50_bills, to_20_bills buttons while dispensing
    bills_window.to_100_bills.setEnabled(False)
    bills_window.to_50_bills.setEnabled(False)
    bills_window.to_20_bills.setEnabled(False)

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
        # re-enable to_100_bills, to_50_bills, to_20_bills buttons after dispensing
        bills_window.to_100_bills.setEnabled(True)
        bills_window.to_50_bills.setEnabled(True)
        bills_window.to_20_bills.setEnabled(True)

        bills_window.hide()
        coins_window.hide()

        # loader_window.hide()
        window.showFullScreen()
    except:
        window.showFullScreen()
def to_50_bills_clicked():
    global coin_count
    global lcd_coin_counter, bills_window, coins_window, window #, loader_window
    bills_window.to_100_bills.setEnabled(False)
    bills_window.to_50_bills.setEnabled(False)
    bills_window.to_20_bills.setEnabled(False)
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
        bills_window.to_100_bills.setEnabled(True)
        bills_window.to_50_bills.setEnabled(True)
        bills_window.to_20_bills.setEnabled(True)

        bills_window.hide()
        coins_window.hide()

        # loader_window.hide()
        window.showFullScreen()
    except:
        window.showFullScreen()
def to_20_bills_clicked():
    global coin_count
    global lcd_coin_counter, bills_window, coins_window, window #, loader_window
    bills_window.to_100_bills.setEnabled(False)
    bills_window.to_50_bills.setEnabled(False)
    bills_window.to_20_bills.setEnabled(False)
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
        bills_window.to_100_bills.setEnabled(True)
        bills_window.to_50_bills.setEnabled(True)
        bills_window.to_20_bills.setEnabled(True)
        
        bills_window.hide()
        coins_window.hide()

        # loader_window.hide()
        window.showFullScreen()
    except:
        window.showFullScreen()

def to_bills_cancel_clicked():
    global bills_window, window
    bills_window.hide()
    window.showFullScreen()

# Define button click handlers
def to_bills_clicked():
    global window, bills_window
     # check if coin count is greater than 0
    if coin_count == 0:
        return
    
    bills_window.to_100_bills.clicked.connect(to_100_bills_clicked)
    bills_window.to_50_bills.clicked.connect(to_50_bills_clicked)
    bills_window.to_20_bills.clicked.connect(to_20_bills_clicked)
    # to_bills_cancel
    bills_window.to_bills_cancel.clicked.connect(to_bills_cancel_clicked)
    window.hide()
    bills_window.showFullScreen()

def to_5_coins_clicked():
    global coin_count, lcd_coin_counter, bills_window, coins_window, window #, loader_window
    # disable to_5_coins and to_1_coins button while dispensing
    coins_window.to_5_coins.setEnabled(False)
    coins_window.to_1_coins.setEnabled(False)
    remaining_coins = dispense(coin_count, [5, 1])
    coin_count = 0
    lcd_coin_counter.display(coin_count)
    if remaining_coins > 0:
        dispense(remaining_coins, [1])

    try:
        # re-enable to_5_coins and to_1_coins button after dispensing
        coins_window.to_5_coins.setEnabled(True)
        coins_window.to_1_coins.setEnabled(True)

        bills_window.hide()
        coins_window.hide()

        # loader_window.hide()
        window.showFullScreen()
    except:
        window.showFullScreen()

def to_1_coins_clicked():
    global coin_count, lcd_coin_counter, bills_window, coins_window, window #, loader_window
    coins_window.to_5_coins.setEnabled(False)
    coins_window.to_1_coins.setEnabled(False)
    dispense(coin_count, [1])
    coin_count = 0
    lcd_coin_counter.display(coin_count)
    try:
        coins_window.to_5_coins.setEnabled(True)
        coins_window.to_1_coins.setEnabled(True)
        bills_window.hide()
        coins_window.hide()
        # loader_window.hide()
        window.showFullScreen()
    except:
        window.showFullScreen()

def to_coins_cancel_clicked():
    global window, coins_window
    window.showFullScreen()
    coins_window.hide()

def to_coins_clicked():
    global coin_count
    if coin_count == 0:
        return
    coins_window.to_5_coins.clicked.connect(to_5_coins_clicked)
    coins_window.to_1_coins.clicked.connect(to_1_coins_clicked)
    # to_coins_cancel button clicked
    coins_window.to_coins_cancel.clicked.connect(to_coins_cancel_clicked)
    window.hide()
    coins_window.showFullScreen()

def dispense(coins, denominations):
    global window, coins_window, bills_window
    if coins == 0:
        return coins
    # try:
    #     loader_window.show()
    # except:
    #     pass
    for denomination in denominations:
        print("Number of {} bills: {}".format(denomination, coins // denomination))
        count = coins // denomination
        time.sleep(1)
        rem = 0
        if count <= 0:
            continue
        rem = operate_dispenser(count, denomination)
        coins = coins % denomination
        if rem <= 0:
            break
        time.sleep(2)
    # try:
    #     loader_window.hide()
    # except:
    #     pass

    return coins


def operate_dispenser(count, denomination):
    dispenser_count = 0
    if denomination == 100:
        while GPIO.input(ir_sensor_1_pin) == GPIO.HIGH:
            time.sleep(0.02)
        GPIO.output(relay_1_pin, GPIO.HIGH)
        while dispenser_count < count:
            if GPIO.input(ir_sensor_1_pin) == GPIO.HIGH:
                dispenser_count += 1
                while GPIO.input(ir_sensor_1_pin) == GPIO.HIGH:
                    time.sleep(0.02)
        if dispenser_count >= count:
            GPIO.output(relay_1_pin, GPIO.LOW)

    elif denomination == 50:
        while GPIO.input(ir_sensor_2_pin) == GPIO.HIGH:
            time.sleep(0.02)
        GPIO.output(relay_2_pin, GPIO.HIGH)
        while dispenser_count < count:
            if GPIO.input(ir_sensor_2_pin) == GPIO.HIGH:
                dispenser_count += 1
                while GPIO.input(ir_sensor_2_pin) == GPIO.HIGH:
                    time.sleep(0.02)
        if dispenser_count >= count:
            GPIO.output(relay_2_pin, GPIO.LOW)
    elif denomination == 20:
        while GPIO.input(ir_sensor_3_pin) == GPIO.HIGH:
            time.sleep(0.02)
        GPIO.output(relay_3_pin, GPIO.HIGH)
        while dispenser_count < count:
            if GPIO.input(ir_sensor_3_pin) == GPIO.HIGH:
                dispenser_count += 1
                while GPIO.input(ir_sensor_3_pin) == GPIO.HIGH:
                    time.sleep(0.02)
        if dispenser_count >= count:
            GPIO.output(relay_3_pin, GPIO.LOW)
    elif denomination == 5:
        while GPIO.input(ir_sensor_4_pin) == GPIO.HIGH:
            time.sleep(0.02)
        GPIO.output(relay_4_pin, GPIO.HIGH)
        while dispenser_count < count:
            if GPIO.input(ir_sensor_4_pin) == GPIO.HIGH:
                dispenser_count += 1
                while GPIO.input(ir_sensor_4_pin) == GPIO.HIGH:
                    time.sleep(0.02)
        if dispenser_count >= count:
            GPIO.output(relay_4_pin, GPIO.LOW)
    elif denomination == 1:
        while GPIO.input(ir_sensor_5_pin) == GPIO.HIGH:
            time.sleep(0.02)
        GPIO.output(relay_5_pin, GPIO.HIGH)
        while dispenser_count < count:
            if GPIO.input(ir_sensor_5_pin) == GPIO.HIGH:
                dispenser_count += 1
                while GPIO.input(ir_sensor_5_pin) == GPIO.HIGH:
                    time.sleep(0.02)
        if dispenser_count >= count:
            GPIO.output(relay_5_pin, GPIO.LOW)
    return count



# Connect button click handlers
window.to_bills.clicked.connect(to_bills_clicked)
window.to_coins.clicked.connect(to_coins_clicked)

window.showFullScreen()
sys.exit(app.exec())

