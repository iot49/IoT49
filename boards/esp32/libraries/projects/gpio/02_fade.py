from machine import Pin, PWM
from board import LED
import time

led = Pin(LED, mode=Pin.OUT)
pwm = PWM(led, freq=1000)

def fade(pwm):
    level = 1023
    while True:
        pwm.duty(level)
        print("level", level)
        level = int(0.9*level)
        time.sleep(0.05)
        if level < 1e-4: break

for _ in range(3):
    fade(pwm)
    
pwm.deinit()
