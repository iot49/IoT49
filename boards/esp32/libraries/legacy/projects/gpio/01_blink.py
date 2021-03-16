from machine import Pin
from board import LED
import time

led_pin = Pin(LED, mode=Pin.OUT)

# blink the led until the end of time ...
while True:
    led_pin(1)
    time.sleep(1)
    led_pin(0)
    time.sleep(1)
