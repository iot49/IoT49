from machine import Pin
from board import LED, A21

led = Pin(LED, mode=Pin.OUT)
button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

while True:
    print('button is', button())
    led(button())
