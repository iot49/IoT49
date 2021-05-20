from machine import Pin, deepsleep
from time import sleep_ms

T = 10000

led = Pin(13, mode=Pin.OUT)
bypass = Pin(21, mode=Pin.IN, pull=Pin.PULL_DOWN)
sleep_ms(500)
if bypass.value() == 1:
    print("REPL")
else:
    print("deepsleep")
    while True:
        led.value(1)
        sleep_ms(T)
        led.value(0)
        led = Pin(13, mode=Pin.IN)
        deepsleep(T)
