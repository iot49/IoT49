from machine import I2C, Timer, Pin
from ina219 import INA219
from board import SDA, SCL
from mqttclient import MQTTClient
from plotclient import PlotClient
from oledfeather import OledFeather, BUTTON_A, BUTTON_B, BUTTON_C
from button import Button

import time, binascii, os

butA = Button(Pin(BUTTON_A, mode=Pin.IN, pull=Pin.PULL_UP))
butB = Button(Pin(BUTTON_B, mode=Pin.IN, pull=Pin.PULL_UP))
butC = Button(Pin(BUTTON_C, mode=Pin.IN, pull=Pin.PULL_UP))

SERIES = "P_vs_RL"
DIR = "mcu/apps/solar/plots/"

# MQTT
mp = None

def mp_connect():
    global mp
    print("connecting to mqtt broker ...")
    BROKER = "iot.eclipse.org"
    mqtt = MQTTClient(server=BROKER)
    print("mqtt", mqtt)
    mqtt.connect()
    mp = PlotClient(mqtt)
    print("mp", mp)

# I2C
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
print("Characterize solar cell")
print("scanning I2C bus ...")
print("I2C:", i2c.scan())

# SSD1306 display
oled = OledFeather(i2c)
oled.text("Solar ...")

# measure power versus load resistance & send to mqtt
def measure():
    global SERIES
    oled.text("Measuring P\nVary RL\nPress A to exit")
    if mp:
        mp.new_series(SERIES, 'Resistance [Ohm]', 'Current [mA]', 'Voltage [V*100]', 'Power [mW]')
    SHUNT_OHMS = 1
    ina = INA219(SHUNT_OHMS, i2c)
    ina.configure()
    # any button press returns to menu
    last_i = 0
    while True:
        if butA.pressed() or butB.pressed() or butC.pressed(): return
        v = ina.voltage()  # [V]
        i = ina.current()  # [mA]
        # avoid division by zero and report only changes
        r = -1 if i < 0.1 else 1000 * v / i
        p = v * i
        if r>0 and mp:
            mp.data(SERIES, r, i, 100*v, p)
        oled.text("R={:5.0f} Ohm\nP={:5.0f} mW\n{:5.1f}V {:5.1f}mA".format(r, p, v, i))
        print("R={:5.0f} Ohm,  P={:5.0f} mW,  V={:5.1f}V,  I={:5.1f}mA".format(r, p, v, i))
        last_i = i
        # limit the measurement rate
        time.sleep(0.2)

# plot recorded data and return to menu
def plot():
    global SERIES, DIR, mp
    print("plot", mp)
    oled.text("plotting ...")
    if mp:
        mp.plot_series(SERIES, \
            filename=DIR + SERIES + ".pdf",
            xlabel="Resistance [Ohm]", \
            ylabel="Current [mA], Voltage [V*100], Power [mW]", \
            title=r"Solar Cell Power versus Load Resistance", \
            xlog=True, grid=True, \
            format=['o', '+', '>'], \
            figsize=(10,8))
    time.sleep(1)

# wait for button presses
print("wait for button presses ...")
while True:
    oled.text("A  measure\nB  plot!\nC  REPL")
    if butA.pressed():
        print("measure")
        if not mp:
            mp_connect()
        measure()
    if butB.pressed():
        print("bot B pressed")
        if not mp:
            mp_connect()
        print("plot")
        plot()
    if butC.pressed():
        print("repl ...")
        oled.text("Passing\ncontrol to\nREPL")
        break


# free up resources and return control to REPL
i2c.deinit()
mqtt.disconnect()
