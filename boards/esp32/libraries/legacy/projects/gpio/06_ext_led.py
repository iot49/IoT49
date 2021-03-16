from machine import Pin
from board import LED, A6
import time

led = Pin(LED, mode=Pin.OUT)
led(1)

ext_led = Pin(A6, mode=Pin.OPEN_DRAIN)
ext_led(1)

while True:
    led(1)
    ext_led(1)
    time.sleep_ms(500)
    led(0)
    ext_led(0)
    time.sleep_ms(500)
