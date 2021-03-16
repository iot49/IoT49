from board import A20, A21
from machine import Pin, RTC
from time import ticks_us, ticks_diff
from time import sleep_us, sleep_ms, strftime, localtime
import time
from network import WLAN, STA_IF, telnet
# from esp import osdebug

"""
IRQ delay test
   Pins p_src and p_dst are connected
   Pin p_src generates a rising edge
   Pin p_dst irq waits for rising edge (from p_src)
   ticks_us is used to measure the ets_delay_us

The test code below sets up the rising edge, "sleeps" for ~ 1ms, and
calculates the irq delay.

WLAN
   Comment out "connect_wlan()"
   below to get faster irq response

PROBLEM:
1) If sleep is implemented as busy wait (simple for loop), everything works
   as expected, typical irq delays are 100 ... 400us, mean ~ 120us.
2) With time.sleep_us(1000) interrupts are never received and the test fails.

Apparently time.sleep_us(...) disables interrupts?!?
"""

"""Number of trials in average"""
N = 10

def connect_wlan():
    """ Connect to wlan. Hard reset to disconnect! """
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect('TPA', 'TurbenThal', 5000)
    while not wlan.isconnected(): continue

def start_rtc():
    """ Start and sync RTC. Requires WLAN. """
    rtc = RTC()
    rtc.ntp_sync(server="pool.ntp.org")
    for _ in range(100):
        if rtc.synced(): break
        sleep_ms(100)
    if rtc.synced():
        pass
        # print(strftime("%c", localtime()))
    else:
        print("Unable to get ntp time")


# osdebug(None)

"""
Pins ... hardwire A20 to A21!
"""
p_src = Pin(A21, mode=Pin.OUT)
p_dst = Pin(A20, mode=Pin.IN)

t_start = 0
t_stop  = 0

def handler(pin):
    global t_stop
    # record time when interrupt was received
    t_stop = ticks_us()

p_dst.irq(handler, trigger=Pin.IRQ_RISING)

def irq_latency(N=500, wlan=False, rtc=False, busy_wait=False):
    global t_start, t_stop
    if wlan: connect_wlan()
    if rtc:  start_rtc()

    d_min = 10000
    d_max =     0
    d_sum =     0

    for _ in range(N):
        p_src(0)
        # record time of rising edge
        t_start = ticks_us()
        # rising edge
        p_src(1)
        for _ in range(1500): pass
        if False:
            if busy_wait:
                print("b", end='')
                for _ in range(1500): pass
            else:
                # os wait
                print("s", end='')
                time.sleep_us(1000)
        # calculate irq delay and statistics
        dt = ticks_diff(t_stop, t_start)
        d_min = min(d_min, dt)
        d_max = max(d_max, dt)
        d_sum += dt

    print("{:5d}   {}     {}     {}   {:8.1f}   {:8.1f}   {:8.1f}".format(
        N,
        "Y" if wlan else "N",
        "Y" if rtc else "N",
        "Y" if busy_wait else "N",
        d_min,
        d_max,
        d_sum/N
    ))

print("    N wlan   rtc b-wait min [us]   max [us]   avg [us]")

irq_latency(N=N, wlan=False, rtc=False, busy_wait=False)
irq_latency(N=N, wlan=False, rtc=False, busy_wait=True)
irq_latency(N=N, wlan=True,  rtc=False, busy_wait=False)
irq_latency(N=N, wlan=True,  rtc=False, busy_wait=True)
irq_latency(N=N, wlan=True,  rtc=True,  busy_wait=False)
irq_latency(N=N, wlan=True,  rtc=True,  busy_wait=True)
