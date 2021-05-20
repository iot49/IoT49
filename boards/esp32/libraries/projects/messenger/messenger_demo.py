from messenger import Messenger
from time import sleep
from random import random
from network import WLAN, STA_IF


def send_read(name, m):
    print("send_read", name, m)
    try:
        n = 1
        for i in range(10):
            if random() < 0.8:
                msg = str.encode("msg {} from {}, tail={}".format(n, name, 'X'*(n**2)))
                m.send(msg)
                n += 1
            m.check_msg()
            sleep(2*random())
    finally:
        m.disconnect()

def cb(msg):
    print("cb got", msg)

ID = "uni49que"

# is_server must be True on one peer, False on the other
# this hack uses the IP to distingish the two
# more typically they would run different software, alleviating the need for this hack ...
is_server = WLAN(STA_IF).ifconfig()[0].endswith('133')

m = Messenger(cb)
m.connect(ID, is_server)
send_read("server" if is_server else "client", m)
