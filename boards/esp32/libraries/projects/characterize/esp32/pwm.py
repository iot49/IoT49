from machine import PWM, Pin
from board import *
from software_time import sleep
from network import WLAN, STA_IF

def connect_wlan():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect('TPA', 'TurbenThal', 5000)
    while not wlan.isconnected(): continue
    print("Connected to WLAN ... IP", wlan.ifconfig()[0])

# optionally connect to wlan ... greatly increases irq latency!
connect_wlan()

# declare pins
pin1 = Pin(A18, mode=Pin.OUT)
pin2 = Pin(A19, mode=Pin.OUT)
pin3 = Pin(A20, mode=Pin.OUT)
pin4 = Pin(A21, mode=Pin.IN)
pin5 = Pin( A5, mode=Pin.OUT)

# interrupt on A21 (connected to A20) replicates A20 to A2
def handler(pin):
    pin5(pin())

pin4.irq(handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# initialize PWM
pwm1 = PWM(pin1, timer=0)
pwm2 = PWM(pin2, timer=0)
pwm3 = PWM(pin3, timer=0)

# set frequency
# Note pwm1.freq() == pwm2.freq() since they use the same timer
pwm1.freq(500)
pwm3.freq(500)

# set duty cycle (0 ... 1023)
pwm1.duty(500)
pwm2.duty(500)
pwm3.duty(500)

print("pwm1:", pwm1)
print("pwm2:", pwm2)
print("pwm3:", pwm3)

try:
    # go about other business (or just take a nap)
    sleep(1000)

finally:
    # release PWM circuitry for later reuse
    pwm1.deinit()
    pwm2.deinit()
    pwm3.deinit()
