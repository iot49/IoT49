from machine import Pin, PWM
from board import LED, A21

led = Pin(LED, mode=Pin.OUT)
led(0)
pwm = PWM(led)

button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

MODE_OFF   = 1
MODE_ON    = 2
MODE_DIM   = 3
MODE_BLINK = 4

mode = MODE_OFF

last_time = time.ticks_ms()

def button_irq_handler(button):
    global mode, last_time
    # ignore button presses in short succession
    new_time = time.ticks_ms()
    if time.ticks_diff(new_time, last_time) < 50:
        # ignore
        print("deglitch")
        return
    last_time = new_time
    # update mode
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


button.irq(button_irq_handler, trigger=Pin.IRQ_FALLING)

print("Return control to REPL; interrupts continue in background")
