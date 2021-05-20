# DRV8833 motor driver
from machine import Pin, PWM

# control one of the two bridges in the DRV8833
class DRV8833:

    FAST_DECAY = 0
    SLOW_DECAY = 1023

    # Arguments:
    #     freq: pwm frequency (integer)
    #     DRV8833 ain1, ain2, bin1, bin2 pin numbers
    def __init__(self, freq, ain1, ain2, bin1, bin2, decay = None):
        """
        Control 2 separate DC motors with DRV8833 H-bridge.
            freq: PWM frequency
            ain1, ain2, bin1, bin2:  pin numbers (e.g. A1, A2, ...)
            decay: DRV8833.SLOW_DECAY (default) or FAST_DECAY
        """
        if decay is None: decay = DRV8833.SLOW_DECAY
        self.motors = [
            Bridge(freq, ain1, ain2, decay),
            Bridge(freq, bin1, bin2, decay)]

    def speed(self, motor, speed=0):
        """speed(motor, speed)

        motor: 0 or 1 (selects bridge A or B)
        speed: -1 ... +1, default: 0 (coast)
        """
        self.motors[motor].set_speed(speed)

    def pwm_freq(self, motor, freq):
        """pwm_freq(motor, freq)

        motor: 0 or 1
        freq:  may be a int [Hz] or function mapping speed to pwm frequency, e.g.
            def speed_to_freq(speed):
                return int(10*speed)
        """
        self.motors[motor].set_pwm_freq(freq)

    def brake(self, motor = None):
        """brake(motor)

        Short motor winding.

        motor: 0, 1, or None (stop both motors)
        """
        if motor:
            self.motors[motor].brake()
        else:
            self.motors[0].brake()
            self.motors[1].brake()

    def deinit(self):
        """
        dinit()

        Release pwm resources.
        """
        self.brake()
        self.motors[0].deinit()
        self.motors[1].deinit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()


# helper class, does the actual work (do not call this directly)
class Bridge:

    def __init__(self, freq, in1, in2, decay = DRV8833.SLOW_DECAY):
        p1 = Pin(in1, mode=Pin.OUT)
        p2 = Pin(in2, mode=Pin.OUT)
        self.in1 = PWM(p1, freq=freq)
        self.in2 = PWM(p2, freq=freq)
        self.freq = None
        # 0 for fast decay, 1023 for slow decay
        self.decay = decay
        self.set_speed(0)

    # set motor speed, fast decay
    def set_speed(self, speed):
        # set speed
        # really should be 1024 for 100% duty cycle,
        # but apparently pwm generator cannot produce this???
        ispeed = min(int(abs(1023*speed)), 1023)
        if self.decay:
            ispeed = 1023 - ispeed
        # adjust frequency
        if self.freq:
            f = int(self.freq(speed))
            self.in1.freq(f)
            self.in2.freq(f)
        if speed < 0:
            self.in1.duty(self.decay)
            self.in2.duty(ispeed)
        else:
            self.in2.duty(self.decay)
            self.in1.duty(ispeed)

    def brake(self):
        self.in1.duty(1023)
        self.in2.duty(1023)

    def set_pwm_freq(self, freq):
        if callable(freq):
            self.freq = freq
        else:
            self.freq = None
            self.in1.freq(int(freq))
            self.in2.freq(int(freq))

    def deinit(self):
        self.brake()
        self.in1.deinit()
        self.in2.deinit()
