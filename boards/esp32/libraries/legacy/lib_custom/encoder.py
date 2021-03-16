# https://forum.micropython.org/viewtopic.php?t=2356
# ? https://github.com/SpotlightKid/micropython-stm-lib/tree/master/encode

from machine import Pin 

class Encoder(object):
    # create encoder for pins pa and pb and attach interrupt handlers
    def __init__(self, pin_x, pin_y):
        self._count = 0
        self.x = Pin(pin_x, mode=Pin.IN)
        self.y = Pin(pin_y, mode=Pin.IN)
        self.x.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback)
        self.y.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback)

    def x_callback(self, _):
        self._count += 1 if self.x() ^ self.y()     else -1

    def y_callback(self, _):
        self._count += 1 if self.x() ^ self.y() ^ 1 else -1

    @property
    def count(self):
        return self._count

    @property
    def count_and_reset(self):
        c = self._count
        self._count = 0
        return c

    def reset(self):
        self._count = 0
