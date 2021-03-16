from machine import Pin
from board import LED, A21
import time

led = Pin(LED, mode=Pin.OUT)
button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

while True:
    read1 = button.value()
    time.sleep(0.01)
    read2 = button.value()
    if read1 and not read2:
        print('Button pressed!')
        led(1)
    elif not read1 and read2:
        print('Button released!')
        led(0)
