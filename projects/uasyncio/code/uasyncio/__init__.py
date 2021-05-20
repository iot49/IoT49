# MicroPython uasyncio module
# MIT license; Copyright (c) 2019 Damien P. George

from .core import *

# lazy loader doesn't work with CircuitPython
from .stream import start_server, open_connection

__version__ = (3, 0, 0)

_attrs = {
    "wait_for": "funcs",
    "wait_for_ms": "funcs",
    "gather": "funcs",
    "Event": "event",
    "Lock": "lock",
    "open_connection": "stream",
    "start_server": "stream",
    "StreamReader": "stream",
    "StreamWriter": "stream",
}

if False:
    for attr,mod in _attrs.items():
        print("load {}.{}".format(mod, attr))
        value = getattr(__import__(mod, None, None, True, 1), attr)
        globals()[attr] = value
    

# Lazy loader, effectively does:
#   global attr
#   from .mod import attr
def __getattr__(attr):
    print("__getattr__", attr)
    mod = _attrs.get(attr, None)
    print("__init__", attr, mod, _attrs)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
