from board import A6, A7
from rpm import RPM
from mqttclient import MQTTClient
from mqttplotter import MQTTPlotter
from rpc_sender import get_resource
from busy_sleep import sleep
from ranges import linrange
import gc

"""
Characterize DC motor RPM vs supply voltage.
On host:
    $ start_plotserver.py
    $ rpc_receiver.py
"""

print("measure RPM vs motor voltage")

RPC_RECEIVER = "http://mac15.home:8080"
MOTOR = "A"

# Encoders ...
rpm_a = RPM(A6)
rpm_b = RPM(A7)
rpm = rpm_a if MOTOR == "A" else rpm_b

# Motor power supply (Rigol DP832A)
print("Connect to DP832A power supply")
pwr = get_resource(RPC_RECEIVER, "pwr")
print("pwr", pwr)
pwr.config(1, v=0, i=0.4, ovp=8, ocp=1, enabled=True)
pwr.config(2, enabled=False)
pwr.config(3, enabled=False)

# setup remote plotter
print("connect to mqtt broker")
mqtt = MQTTClient("iot.eclipse.org")
plotter = MQTTPlotter(mqtt)
RPM_VOLTAGE = "rpm_voltage"
plotter.new_series(RPM_VOLTAGE, "Voltage  [V]", "RPM", "Current  [mA]")

# run test
print("run test ...")
for v in linrange(0.5, 6.5, 12):
    gc.collect()
    print("Test voltage = {:8.2f} V".format(v))
    # set motor voltage
    pwr.config(1, v=v)
    # wait a little to make sure motor runs at constant speed
    sleep(1)
    # reset rpm counter
    rpm.reset()
    # wait a little to get a good rpm measurement
    sleep(6)
    plotter.data(RPM_VOLTAGE, pwr.v(1), rpm.rpm(), 1000*pwr.i(1))

# turn of power to motor
pwr.config(1, v=0, enabled=False)
pwr.release_resource()

# plot
plotter.plot_series(RPM_VOLTAGE,
    filename="esp32/projects/motors/plots/rpm_voltage_{}.pdf".format(MOTOR),
    format=['o', '+'],
    figsize=(8,5),
    title="Motor RPM versus Voltage (no load)",
    xlabel="Voltage  [V]",
    ylabel="RPM   /   Current [mA]")

# do not disconnect before plot is generated ...
sleep(5)
mqtt.disconnect()
