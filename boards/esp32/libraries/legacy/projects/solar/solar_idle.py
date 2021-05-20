import time, machine, gc
from machine import I2C, Timer
from ina219.ina219 import INA219
from mqtt import MQTTClient
from board import VBAT2, SDA, SCL

# update these to match your ThinkSpeak channel configuration
TS_CHANNEL_ID = "329194"
TS_WRITE_KEY = "OHF2H4SGNQVNW0RV"
TS_TOPIC = "channels/" + TS_CHANNEL_ID + "/publish/" + TS_WRITE_KEY

def measure(args):
    global ina, led, wdt, last_hour, mqtt_client
    # reconnect to wifi if we got disconnected
    wifi_rtc(True)
    # measure solar cell voltage and current
    v = ina.voltage()
    i = ina.current()
    # publish the results
    print("{:8.4}V {:8.4}mA".format(v, i))
    mqtt_client.publish(TS_TOPIC, "field1={}&field2={}".format(v,i))
    # log on each hour
    _, _, _, hour, *rest = time.localtime()
    if hour is not last_hour:
        log("idle {:8.4}V {:8.4}mA".format(v, i))
        last_hour = hour
    # indicate activity on LED
    led.toggle()
    # feed the WDT
    wdt.feed()
    # conserve power?
    machine.idle()

# setup ina for V/I measurement
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS, i2c)
ina.configure()

# connect to the cloud
mqtt_client = MQTTClient("", "mqtt.thingspeak.com", port=1883)
try:
    mqtt_client.connect()
except:
    print("connot connect to MQTT broker")
    log("cannot connect to MQTT broker")

# keep track of uptime
log("solar_idle started")

# period [msec] between calls to measure
# note: ThingSpeak free account limited to updates at 15sec intervals
period = 15000
last_hour = 0

# start WDT
wdt = WDT(timeout=period+2000)

# start mesuring
measure(None)
Timer.Alarm(measure, period/1000, periodic=True)

# program runs in background ... proceed to REPL
# should never get here if measure calls idle?
print("Solar monitor is running in background. Calling machine.idle()")
machine.idle()
