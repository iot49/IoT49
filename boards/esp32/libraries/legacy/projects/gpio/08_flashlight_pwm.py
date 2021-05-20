from machine import Pin, PWM
from board import LED, A21

# this time using pwm to blink: keep polling for button presses while blinking

led = Pin(LED, mode=Pin.OUT)
led(0)

button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

# NOTE: deinit pwm before running again (e.g. reset)
pwm = PWM(led)

MODE_OFF   = 1
MODE_ON    = 2
MODE_DIM   = 3
MODE_BLINK = 4

mode = MODE_OFF
last_button = -1

while True:
    b = button()
    if not b and last_button:
        mode += 1
        if mode > MODE_BLINK: mode = MODE_OFF
        print("new mode is", mode)
        if mode is MODE_ON:
            pwm.freq(1)
            pwm.duty(1023)
        elif mode is MODE_DIM:
            pwm.freq(100)
            pwm.duty(100)
        elif mode is MODE_BLINK:
            pwm.freq(5)
            pwm.duty(500)
        else:
            pwm.freq(1)
            pwm.duty(0)
    last_button = b

pwm.deinit()
