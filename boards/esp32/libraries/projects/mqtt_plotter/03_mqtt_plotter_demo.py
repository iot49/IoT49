from mqttplotter import MQTTPlotter
from mqttclient import MQTTClient
from math import sin, cos, exp, pi

mqtt = MQTTClient("iot.eclipse.org")
mp = MQTTPlotter(mqtt)

SERIES = "sinusoid"

mp.new_series(SERIES, 'time', 'cos', 'sin', 'sin*cos')
def f1(t): return cos(2 * pi * t) * exp(-t)
def f2(t): return sin(2 * pi * t) * exp(-t)
def f3(t): return sin(2 * pi * t) * cos(2 * pi * t) * exp(-t)
for t in range(200):
    t *= 0.025
    mp.data(SERIES, t, f1(t), f2(t), f3(t))

mp.save_series(SERIES)
mp.plot_series(SERIES, \
    xlabel="Time [s]", \
    ylabel="Voltage [mV]", \
    title=r"Damped exponential decay $e^{-t} \cos(2\pi t)$")

print("disconnect")
mqtt.disconnect()
