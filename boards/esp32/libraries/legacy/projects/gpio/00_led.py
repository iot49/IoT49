from machine import Pin
from board import LED

led = Pin(LED, mode=Pin.OUT)  # declare LED pin
led(1)                        # turn LED on
