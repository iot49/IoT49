from machine import Pin
import time

class RPM:
    """
    Measure average rpm sijnce last call to reset().
    For single (not quadrature) encoder.
    """
    def __init__(self, enc_pin, cpt=48):
        """
        enc_pin: in to which encoder is connected.
        cpt: counts per turn
        """
        self.cpt = cpt
        self.reset()
        pin = Pin(enc_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        pin.irq(self.__irq, Pin.IRQ_FALLING or Pin.IRQ_RISING)

    def __irq(self, pin):
        """
        Interrupt callback. Used internally.
        """
        self.__count += 1

    def reset(self):
        """
        Reset count.
        Call at beginning of measurement interval.
        """
        self.__count = 0
        self.__start_time = time.ticks_us()

    def rpm(self):
        """
        Average rpm since last call of reset().
        Does NOT call reset!
        """
        count = self.__count
        dt = time.ticks_diff(time.ticks_us(), self.__start_time)
        return 1e6*60/self.cpt * count / dt if dt > 0 else None

    def count(self):
        """
        Encoder count since last call to reset.
        """
        return self.__count
