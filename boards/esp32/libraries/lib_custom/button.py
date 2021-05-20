import time

"""
Buttons state detect with debouncing.

Info on bouncing:
http://www.ganssle.com/debouncing.htm
http://www.ganssle.com/debouncing-pt2.htm
"""


class Button:

    # arguments:
    def __init__(self, pin, callback=None, falling=True, debounce_ms=50):
        """
        pin, configured (e.g. PULL_UP/DOWN)
        falling: detects button presses for switches that are normally high
        """
        self.last_time_ms = 0
        self.detected = False  # a button press was detected
        self.cb = callback
        self.debounce_ms = debounce_ms
        pin.irq(self._irq_cb, pin.IRQ_FALLING if falling else pin.IRQ_RISING)

    #
    def pressed(self):
        """True if a button press was dectected since the last call of this function"""
        p = self.detected
        self.detected = False
        return p

    def _irq_cb(self, pin):
        """irq handler with debouncing"""
        t = time.ticks_ms()
        if abs(t - self.last_time_ms) < self.debounce_ms: return
        self.last_time_ms = t
        self.detected = True
        if self.cb: self.cb(pin)
