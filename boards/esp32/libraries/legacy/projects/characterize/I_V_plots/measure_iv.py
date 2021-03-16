from machine import I2C, Pin
from ina219 import INA219
from board import SDA, SCL
from rpc_sender import get_resource
from busy_sleep import sleep
from ranges import linrange
from mqttclient import MQTTClient
from mqttplotter import MQTTPlotter

"""
Plot I/V charcteristic of device.
(Board K, I/V characteristic.)

1) Connect DP832A channel 1 between Vin+ (strip row 22) and DUT GND
2) Connect DUT between +/- srip on battery connector side of esp32

3) Start servers on host (mac):
    $ start_plotserver.py
    $ rpc_receiver.py

4) Edit config below.

5) Turn on DP832A. Run this file.
"""

VOLTAGES = linrange(0, 6, 20)   # range objects for all test voltages [V]
Imax = 0.050       # maximum test current [A]
N = 5              # number of voltage steps
SHUNT_OHMS = 0.1   # INA219 shunt resistor value [Ohm]

# output plot ...
FILENAME = "esp32/projects/iv_characteristic/plots/led_yellow.pdf"
PLOT_TITLE = "Yellow LED"

try:
    SERIES = "IV"
    mqtt = MQTTClient("iot.eclipse.org")
    mp = MQTTPlotter(mqtt)

    # I2C
    i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
    print("scanning I2C bus ...")
    print("I2C:", i2c.scan())

    # INA219 current sensor
    ina = INA219(SHUNT_OHMS, i2c)
    ina.configure()

    # Rigol power supply
    print("Connect to DP832A power supply")
    pwr = get_resource("http://mac15.home:8080", "pwr")
    pwr.config(1, enabled=True, v=0, i=Imax, ovp=20, ocp=3*Imax)
    pwr.config(2, enabled=False)
    pwr.config(3, enabled=False)

    # perform measurements ...
    mp.new_series(SERIES, 'Voltage [V]', 'Current [mA]')

    for vtest in VOLTAGES:
        pwr.config(1, v=vtest)
        sleep(1)
        v = ina.voltage()  # [V]
        i = ina.current()  # [mA]
        print("V = {:8.3f} V    I = {:8.3f} mA".format(v, i))
        mp.data(SERIES, v, i)

    # turn off power supply
    pwr.config(1, enabled=False)

    # plot recorded data and return to menu
    mp.plot_series(SERIES,
            filename=FILENAME,
            xlabel="Voltage  [V]",
            ylabel="Current  [mA]",
            title=PLOT_TITLE,
            xlog=False, grid=True,
            format=['o'],
            figsize=(10,8))

finally:
    # free up resources and return control to REPL
    i2c.deinit()
    mqtt.disconnect()
