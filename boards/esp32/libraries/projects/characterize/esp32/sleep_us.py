from board import A19
from machine import Pin
import time

p = Pin(A19, mode=Pin.OUT)

dt = 12

while True:
    p(1)
    time.sleep_ms(dt)
    p(0)
    time.sleep_ms(dt)
