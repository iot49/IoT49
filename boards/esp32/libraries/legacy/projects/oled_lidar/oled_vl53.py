from machine import I2C, Pin, RTC
from board import SDA, SCL
from oledfeather import OledFeather
from vl53l0x import VL53L0X
import time


i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

oled = OledFeather(i2c)
oled.text("Lidar Demo")

vlx = VL53L0X(i2c)
vlx.init()
vlx.start()

while True:
    d = vlx.read()
    if d > 20 and d < 1500:
        oled.text("Lidar Demo\n{:6d} mm".format(d))
    time.sleep(1)
