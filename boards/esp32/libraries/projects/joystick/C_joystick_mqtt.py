from machine import Pin, ADC
from board import LED, A21, ADC0, ADC3
from mqttclient import MQTTClient
import gc, time, machine

led = Pin(LED, mode=Pin.OUT)

BROKER = "mac15.home"
BROKER = "dev.home"
BROKER = "iot.eclipse.org"
print("Connecting to broker", BROKER, "...")
mqtt = MQTTClient(BROKER)
print("Connected!")

def mqtt_callback(topic, msg):
    global led, run
    if topic == b'repl':
        run = False
        print("got run false")

mqtt.set_callback(mqtt_callback)
mqtt.subscribe("repl")

# Joystick
button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)
xout = ADC(Pin(ADC0))
yout = ADC(Pin(ADC3))
xout.atten(ADC.ATTN_6DB)
yout.atten(ADC.ATTN_6DB)

# offset
xoff  = 1920
yoff  = 2005
scale = 1900

# filter
alpha = 0.5
xfilt = 0
yfilt = 0

# history
old_x = old_y = 0
old_button = None

# run program
run = True
next_blink = 0   # time when next to blink the led

while run:
    gc.collect()
    # check for messages
    mqtt.check_msg()
    xfilt = (1-alpha) * xfilt + alpha * (xout.readraw()-xoff)
    yfilt = (1-alpha) * yfilt + alpha * (yout.readraw()-yoff)
    xx = xfilt/scale
    yy = yfilt/scale
    print("x={:8.3f}  y={:8.3f}".format(xx, yy))
    # print("x={:40s}|   y={:40s}|".format(int(20*(xx+1))*'*', int(20*(yy+1))*'*'))
    if abs(old_x - xx) > 0.005:
        print("publish x", xx)
        mqtt.publish("x", str(xx))
        old_x = xx
    if abs(old_y - yy) > 0.005:
        print("publish y", yy)
        mqtt.publish("y", str(yy))
        old_y = yy
    if old_button is not button():
        mqtt.publish("stop", str(not button()))
        old_button = button()
    # slowly blink the led
    if time.ticks_diff(time.ticks_ms(), next_blink) > 0:
        next_blink = time.ticks_add(time.ticks_ms(), 1000)
        led(not led())
    time.sleep_ms(200)

print("Joystick: stop MQTT client and return to REPL")
mqtt.disconnect()
