from mqttclient import MQTTClient
import time

def mqtt_callback(topic, msg):
    print("MQTT received topic={}, msg='{}'".format(topic, msg))

SERVER = "iot.eclipse.org"

mqtt = MQTTClient(SERVER)
mqtt.set_callback(mqtt_callback)
mqtt.subscribe("y")

# publish
for i in range(20):
    mqtt.check_msg()
    msg = "value=" + str(i)
    topic = "x"
    print("publish topic={} msg={}".format(topic, msg))
    mqtt.publish(topic, msg)
    time.sleep(1)

mqtt.disconnect()
