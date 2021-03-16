from mqttclient import MQTTClient
import binascii, machine, time, gc

mqtt = MQTTClient("iot.eclipse.org")

def mqtt_callback(topic, msg):
    print("callback:", topic, msg)
    global run
    if topic == b'stop':
        run = False
    else:
        print("received unknown topic={:s}, msg='{:s}'".format(topic, msg))

mqtt.set_callback(mqtt_callback)
mqtt.subscribe("stop")

run = True
count = 0

while run:
    mqtt.check_msg()
    mqtt.publish("x", str(count))
    count += 1
    if count > 100: run = False
    time.sleep(1)

print("mqtt demo: stop MQTT client and return to REPL")
mqtt.disconnect()
