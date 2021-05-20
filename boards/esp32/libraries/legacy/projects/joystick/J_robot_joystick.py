from machine import Pin
from board import *
from drv8833 import DRV8833
from mqttclient import MQTTClient
import time, gc
from math import fabs

# robot controlled by joystick

# remote led control
led = Pin(LED, mode=Pin.OUT)

# mqtt
BROKER = "iot.eclipse.org"
BROKER = "mac15.home"
BROKER = "habiandev.local"
BROKER = "dev.home"
mqtt = MQTTClient(BROKER)
print("connected to broker at", BROKER)

run = True
x = y = 0
brake = False

def set_speed():
    global motors, x, y, brake
    if brake:
        motors.brake(0)
        motors.brake(1)
        return
    sp0 = x + y
    sp1 = x - y
    if fabs(sp0) < 0.1: sp0 = 0
    if fabs(sp1) < 0.1: sp1 = 0
    print("setspeed x={:6.3f}, y={:6.3f} --> sp0={:6.3f} sp1={:6.3f}".format(x, y, sp0, sp1))
    motors.speed(0, sp0)
    motors.speed(1, sp1)

def mqtt_callback(topic, msg):
    msg = msg.decode("utf-8")
    global led, run, motors, x, y, brake
    if topic == b'stop':
        brake = msg == 'True'
        led(brake)
        if brake:
            print("apply emergency brake")
            motors.brake(0)
            motors.brake(1)
        else:
            print("release brake")
    elif topic == b'x':
        x = float(msg)
        set_speed()
    elif topic == b'y':
        y = float(msg)
        set_speed()
    elif topic == b'repl2':
        run = False


mqtt.set_callback(mqtt_callback)
mqtt.subscribe("repl")
mqtt.subscribe("x")
mqtt.subscribe("y")
mqtt.subscribe("stop")


# motor controller

freq = 100
stop = False
motors = None

def speed_to_freq(speed):
    f = 2500*fabs(speed)-450
    return min(max(20, f), 500)


with DRV8833(freq, A20, A21, A19, A18) as m:
    m.pwm_freq(0, speed_to_freq)
    m.pwm_freq(1, speed_to_freq)
    motors = m
    while run:
        if gc.mem_free() < 20000:
            gc.collect()
        # check for messages
        mqtt.check_msg()
        time.sleep_ms(50)

mqtt.disconnect()

print("returning control to repl")
