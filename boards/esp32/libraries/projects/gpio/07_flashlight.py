from machine import Pin
from board import LED, A21
import time

led = Pin(LED, mode=Pin.OUT)
led(0)
button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

MODE_OFF   = 1
MODE_ON    = 2
MODE_DIM   = 3
MODE_BLINK = 4

mode = MODE_OFF
last_button = -1

while True:
    b = button()
    if not b:
        if last_button and not b:
            print("change!")
            mode += 1
            if mode > MODE_BLINK:
                mode = MODE_OFF
            print("new mode is", mode)
    last_button = b
    if mode is MODE_ON:
        led(1)
    elif mode is MODE_DIM:
        led(1)
        time.sleep_ms(1)
        led(0)
        time.sleep_ms(9)
    elif mode is MODE_BLINK:
        led(1)
        time.sleep(1)
        led(0)
        time.sleep(1)
    else:
        led(0)
