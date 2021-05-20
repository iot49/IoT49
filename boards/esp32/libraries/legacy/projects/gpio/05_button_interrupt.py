from machine import Pin
from board import LED, A21
from micropython import schedule

led = Pin(LED, mode=Pin.OUT)
button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)

count = 0

def report(pin):
    global count
    if pin() == 0:
        print("> pressed {} times".format(count))
    else:
        print("         < released {} times".format(count))

def button_irq_handler(button):
    global count
    if button() == 0: count += 1
    led(1-button())
    schedule(report, button)

button.irq(button_irq_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

print("Return control to REPL; interrupts continue in background")
