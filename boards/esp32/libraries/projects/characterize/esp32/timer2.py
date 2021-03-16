from machine import Timer
from time import ticks_us, sleep_ms, ticks_diff
from micropython import schedule
from array import array
import gc
from board import A19
from machine import Pin
import os

"""
Measure machine.Timer delay statistics.
"""

# period [ms]
period = 50

pin = Pin(A19, mode=Pin.OUT)

last_free = gc.mem_free()
iteration = 0
last_us = None

def calc():
    """Called during each iteration of the timer.

    Simulates code run by timer in a real application.
    """
    global last_free, iteration, pin
    mf = gc.mem_free()
    if False and last_free < mf:
        print(">>> ran gc, iteration=", iteration)
    last_free = mf
    # allocate memory
    x = "abc" + str(iteration)
    pin(not pin())
    sleep_ms(2)

def timer_cb(timer):
    global last_us, period, iteration
    calc()
    now_us = ticks_us()
    if last_us:
        error_us = ticks_diff(now_us, last_us) - 1000*period
        if abs(error_us) > 0: print("{:4d} error {:6d}us".format(iteration, error_us))
        iteration += 1
    last_us = now_us
    gc.collect()

try:
    print("os.uname:", os.uname())
    timer = Timer(1)
    print("timer:", timer)
    timer.init(period=period, mode=Timer.PERIODIC, callback=timer_cb)
    while True: sleep_ms(1)
finally:
    timer.deinit()
