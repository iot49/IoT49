from board import SDA, SCL
from ina219 import INA219
from machine import Pin, I2C, RTC, deepsleep
from time import sleep, ticks_ms, ticks_diff, strftime
from network import WLAN, STA_IF


"""
ESP32 power dissipation
   Connect constant 3.3V DC source to test board.
   Communicate through USB (as wifi down for part of test).
   INA219 measures ESP32 current (not including its own current).
"""

# I2C
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
print("scanning I2C bus ...")
print("I2C:", i2c.scan())

# INA219 current sensor
SHUNT_OHMS = 0.1 * 107/89   # calibrated INA219 shunt resistor value [Ohm]
ina = INA219(SHUNT_OHMS, i2c)
ina.configure()

def print_iv(state):
    global ina
    v = ina.voltage()
    i = ina.current()
    print("{:40s}   {:8.0f}mA    {:8.3}V".format(state, i, v))

# no wifi

for _ in range(3):
    print_iv("cpu on, wifi off")
    sleep(1)

# start wlan

wlan = WLAN(STA_IF)
wlan.active(True)

for _ in range(3):
    print_iv("cpu on, wlan active, no connection")
    sleep(1)

# connect to wifi

t_start = ticks_ms()
wlan.connect('TPA', 'TurbenThal', 5000)
while not wlan.isconnected(): continue
t_stop = ticks_ms()

print("{:8.3}s for connecting to wlan".format(ticks_diff(t_stop, t_start)/1e3))
print("IP", wlan.ifconfig()[0])

for _ in range(3):
    print_iv("cpu on, wifi connected")
    sleep(1)

# fetch internet time

t_start = ticks_ms()
rtc = RTC()
rtc.ntp_sync(server="hr.pool.ntp.org")
while not rtc.synced(): continue
t_stop = ticks_ms()

print("{:8.3}s for connecting getting internet time".format(ticks_diff(t_stop, t_start)/1e3))
print(strftime("%c", rtc.now()))

for _ in range(3):
    print_iv("cpu on, wifi connected")
    sleep(1)

wlan.disconnect()

for _ in range(3):
    print_iv("cpu on, wifi disconnected")
    sleep(1)

wlan.active(False)

for _ in range(3):
    print_iv("cpu on, wlan inactive")
    sleep(1)

# deepsleep

print("deepsleep; reset to wake up")
deepsleep(0)
