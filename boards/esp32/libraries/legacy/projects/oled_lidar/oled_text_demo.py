from machine import I2C, Pin, RTC
from board import SDA, SCL
from oledfeather import OledFeather
import time


i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

oled = OledFeather(i2c)

while True:
    oled.text(time.strftime('%A\n%b %d, %Y\n%H:%M:%S', RTC().now()))
    time.sleep(1)
