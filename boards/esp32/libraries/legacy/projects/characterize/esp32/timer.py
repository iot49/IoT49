from machine import Timer
import time

def timer_cb(timer):
    """Called at intervals set by period."""
    # ... do whatever needs to be done regularly ...
    print("timer", timer)
    pass

# timer_cb is called every "period" [ms]
# BUG: timer_cb never called for period > 26 ???
period = 100

timer = Timer(1)
timer.init(period=period, mode=Timer.PERIODIC, callback=timer_cb)

# timer_cb continues to be called at the specified interval
# while doing other work
for i in range(100):
    print("sleep", i)
    time.sleep(0.01)

print("stop timer")
timer.deinit()
