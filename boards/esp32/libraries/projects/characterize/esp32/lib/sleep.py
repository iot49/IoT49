from board import A19
from machine import Pin
import time

"""
Test timing accuracy of various 'sleep' implementations.
"""

pin = Pin(A19, mode=Pin.OUT)

while True:
    pin(1)
    time.sleep_us(100)
    pin(0)
    time.sleep_us(1000)
