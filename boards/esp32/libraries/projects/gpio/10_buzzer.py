from board import A20
from machine import Pin, PWM
from software_time import sleep

buzzer = Pin(A20, mode=Pin.OUT)
synthesizer = PWM(buzzer, freq=440)

for _ in range(5):
    synthesizer.freq(880)
    sleep(0.5)
    synthesizer.freq(440)
    sleep(0.5)

synthesizer.duty(0)

synthesizer.deinit()
