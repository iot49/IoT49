from messenger import Messenger
from mqttclient import MQTTClient
from random import random
from network import WLAN, STA_IF
import time, gc

# is_server must be True on one peer, False on the other
# this hack uses the IP to distingish the two
# more typically they would run different software, alleviating the need for this hack ...
is_server = WLAN(STA_IF).ifconfig()[0].endswith('133')


# messenger benchmark
def messenger_benchmark(N, is_server):
    received = 0
    def cb(msg):
        nonlocal received
        received += 1

    m = Messenger(cb)
    m.connect("uni49que", is_server)
    print("Starting test ...")
    gc.collect()
    try:
        t_start = time.ticks_ms()
        for i in range(N):
            if is_server:
                m.send("msg {}".format(i))
                m.wait_msg()
            else:
                m.wait_msg()
                m.send("ok {}".format(i))
        t_stop = time.ticks_ms()
        dt = time.ticks_diff(t_stop, t_start)
        if N != received:
            print("***** sent {} messages, received {}".format(N, received))
        print(">>> Messenger throughput: {:8.4f} msg/s (N={})".format(1000*received/dt, N))
    finally:
        m.disconnect()


# MQTT benchmark
def mqtt_benchmark(N, is_server, broker, user, pwd):
    received = 0
    def mqtt_callback(topic, msg):
        nonlocal received
        received += 1

    print("Connecting to MQTT broker", broker, "...")
    mqtt = MQTTClient(broker, user=user, password=pwd)
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe("iot49/{}".format(is_server))
    topic = "iot49/{}".format(not is_server)
    print("Starting test ...")
    gc.collect()
    try:
        t_start = time.ticks_ms()
        for i in range(N):
            if is_server:
                mqtt.publish(topic, "msg {}".format(i))
                mqtt.wait_msg()
            else:
                mqtt.wait_msg()
                mqtt.publish(topic, "ok {}".format(i))
        t_stop = time.ticks_ms()
        dt = time.ticks_diff(t_stop, t_start)
        if N != received:
            print("***** sent {} messages, received {}".format(N, received))
        print(">>> MQTT throughput, broker {}: {:8.4f} msg/s (N={})".format(broker, 1000*received/dt, N))
    finally:
        mqtt.disconnect()

# run the benchmarks
N = 100
BROKER1 = "iot.eclipse.org"
BROKER2 = "dev.home"
USER2 = "openhabian"
PWD2 = "furfande"

messenger_benchmark(N, is_server)
mqtt_benchmark(N, is_server, BROKER1, None, None)
mqtt_benchmark(N, is_server, BROKER2, USER2, PWD2)
