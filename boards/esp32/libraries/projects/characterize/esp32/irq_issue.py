from board import A20, A21
from machine import Pin
import machine, time

"""
IRQ delay test
   Pins p_src and p_dst are connected
   Pin p_src generates a rising edge
   Pin p_dst irq waits for rising edge (from p_src)
   ticks_us is used to measure the ets_delay_us

The test code below sets up the rising edge, "sleeps" for ~ 1ms, and
calculates the irq delay.

PROBLEM:
1) If sleep is implemented as busy wait (simple for loop), everything works
   as expected, typical irq delays are 100 ... 400us, mean ~ 120us.
2) With time.sleep_us(1000) interrupts are never received and the test fails.

Apparently time.sleep_us(...) disables interrupts?!?
"""
busy_sleep = False

p_src = Pin(A21, mode=Pin.OUT)
p_dst = Pin(A20, mode=Pin.IN)

t_start = 0
t_stop  = 0

def busy_sleep_us(us):
    """
    Busy sleep us [micro-second].
    Apparently time.sleep turns off all sorts of stuff. Then use this.
    """
    start = time.ticks_us()
    while time.ticks_diff(time.ticks_us(), start) < us:
        pass

def handler(pin):
    global t_stop
    # record time when interrupt was received
    t_stop = time.ticks_us()

p_dst.irq(handler, trigger=Pin.IRQ_RISING)

d_min = 10000
d_max =     0
d_sum =     0
N = 50

for _ in range(N):
    p_src(0)
    # record time of rising edge
    t_start = time.ticks_us()
    # rising edge
    p_src(1)
    time.sleep_us(10000)
    if busy_sleep:
        busy_sleep_us(1000)
    else:
        time.sleep_us(1000)
    # calculate irq delay and statistics
    dt = time.ticks_diff(t_stop, t_start)
    d_min = min(d_min, dt)
    d_max = max(d_max, dt)
    d_sum += dt

print("{} tests, min={}us, max={}us, avg={:6.1f}us".format(N, d_min, d_max, d_sum/N))
