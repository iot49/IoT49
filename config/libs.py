# Package declaration syntax:
#
#     Package(
#       user-friendly-name, 
#       path (relative to $IOT49), 
#       target folder on MCU, usually 'lib')

# shared secrets file
Package("secrets", "config/secrets.py")

# airlift
Package("airlift-client", "projects/airlift/code/client", "lib")
Package("airlift-server", "projects/airlift/code/server", "lib")

# mp wireless "repl"
Package("mp-server", "projects/mp-repl/code", "lib")

# blinka - Adafuit drivers on MicroPython
Package("blinka", "projects/blinka/code", "lib")

# uasyncio on CircuitPython
Package("uasyncio", "projects/uasyncio/code", "lib")

# MicroPython 
Package("bno055",  "boards/libs/bno055", "lib")
Package("vl53l0x", "boards/libs/vl53l0x", "lib")
Package("vl53l1x", "boards/libs/vl53l1x", "lib")

# CircuitPython
Package("adafruit-circuitpython-ble", "boards/libs/adafruit-circuitpython-ble", "lib")

Package("pystone", "boards/libs/pystone/", "lib")

