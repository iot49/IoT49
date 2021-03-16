from machine import I2C, Pin, RTC
from board import SDA, SCL
from vl53l0x import VL53L0X
import time


i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

vlx = VL53L0X(i2c)
vlx.init()
vlx.start()

while True:
    d = vlx.read()
    if d > 20 and d < 1500:
        print("Lidar: {:6d} mm".format(d))
    time.sleep(0.3)
