import time

class SoftwareTimer:
    '''
    Run callback function at periodic interval
    sw_timer is a reference to the timer object (useful for changing period or stop)
    dt_us is the actual delay since the last call in [us]
    slept_us is the duration the timer spent sleeping in [us]
    
    def cb(sw_timer, dt_us, slept_us):
        print(dt_us)

    st = SoftwareTimer(5, cb)
    st.run()
    '''

    def __init__(self, period_ms, callback):
        """
        Call callback at specified interval in [ms]
        """
        self.period_ms = period_ms
        self.callback = callback

    def set_period_ms(self, period_ms):
        self.period_ms = period_ms

    def get_period_ms(self):
        return self.period_ms

    def run(self):
        last_time_us = time.ticks_us()
        while self.period_ms > 0:
            # time to sleep, minus empirical offset to correct static error
            this_time_us = time.ticks_add(last_time_us, 1000*self.period_ms)
            dt_us = time.ticks_diff(this_time_us, time.ticks_us()) - 130
            time.sleep_us(dt_us)
            now_us = time.ticks_us()
            self.callback(self, time.ticks_diff(now_us, last_time_us), dt_us)
            last_time_us = now_us

    def stop(self):
        self.period_ms = -1


def sleep_us(us):
    """
    Busy sleep us [micro-second].
    Apparently time.sleep turns off all sorts of stuff. Then use this.
    """
    start = time.ticks_us()
    while time.ticks_diff(time.ticks_us(), start) < us:
        pass

def sleep_ms(ms):
    """
    Busy sleep ms [milli-second].
    Apparently time.sleep turns off all sorts of stuff. Then use this.
    """
    sleep_us(1e3*ms)

def sleep(sec):
    """
    Busy sleep sec [second].
    Apparently time.sleep turns off all sorts of stuff. Then use this.
    """
    sleep_us(1e6*sec)
