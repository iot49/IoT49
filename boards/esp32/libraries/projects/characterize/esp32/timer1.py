from machine import Timer
from time import ticks_us, sleep_ms, ticks_diff
from micropython import schedule
from array import array
import gc
from board import A19
from machine import Pin

"""
Measure machine.Timer delay statistics.
"""

# period [ms]
period = 15
# number of tests
N = 2000

pin = Pin(A19, mode=Pin.OUT)

last_free = gc.mem_free()

def calc():
    """Called during each iteration of the timer.

    Simulates code run by timer in a real application.
    """
    global last_free
    mf = gc.mem_free()
    if last_free < mf:
        print("ran gc, index=", index)
    last_free = mf
    # allocate memory
    x = "abc" + str(index)
    global pin
    pin(not pin())
    sleep_ms(2)

# array of period errors [us]
errors = array('i', range(N))
index = 0
last_us = None
period_us = 1000*period

def timer_cb(timer):
    global errors, index, last_us, N, period_us
    now_us = ticks_us()
    if last_us:
        if index < N:
            error = ticks_diff(now_us, last_us) - period_us
            errors[index] = error
            if error > 100: print("Big error:", error)
        index += 1
    last_us = now_us
    calc()

try:
    timer = Timer(1)
    timer.init(period=period, mode=Timer.PERIODIC, callback=timer_cb)
    while index < N: sleep_ms(1)
    print(errors)
    # keep running (for the oscilloscope to have something to look at)
    while True: sleep_ms(1)
finally:
    timer.deinit()

print(errors)
