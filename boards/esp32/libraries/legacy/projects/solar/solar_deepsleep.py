import machine, time
from machine import I2C, Timer, Pin
from ina219.ina219 import INA219
from mqtt import MQTTClient
from board import A21,VBAT2,SDA,SCL

# update these to match your ThinkSpeak channel configuration
TS_CHANNEL_ID = "329194"
TS_WRITE_KEY = "OHF2H4SGNQVNW0RV"
TS_TOPIC = "channels/" + TS_CHANNEL_ID + "/publish/" + TS_WRITE_KEY

# period [msec] between calls to measure (plus time to boot)
# note: ThingSpeak free account limited to updates at 15sec intervals
period = 15000

try:
    mqtt_client = MQTTClient(TS_WRITE_KEY + TS_CHANNEL_ID, "mqtt.thingspeak.com", port=1883)
    mqtt_client.connect()
    # setup ina for V/I measurement
    i2c = I2C(0, I2C.MASTER, baudrate=100000)
    SHUNT_OHMS = 0.1
    ina = INA219(SHUNT_OHMS, i2c)
    ina.configure()
    # measure solar cell voltage and current
    v = ina.voltage()
    i = ina.current()
    mqtt_client.publish(TS_TOPIC, "field1={}&field2={}".format(v,i))
except:
    print("ERROR in deepsleep")
    log("ERROR in deepsleep")

# Backdoor - Pin 15: don't call deepsleep if pulled up
P15 = Pin('P15', mode=Pin.IN, pull=Pin.PULL_DOWN)

if P15() is 0:
    # seems like 100ms+ sleep is required for mqtt data to be sent (???)
    time.sleep_ms(500)
    led(0)
    machine.deepsleep(period)
else:
    # pass control to REPL
    pass
