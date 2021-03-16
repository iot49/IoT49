ESP32 Power Dissipation (Huzzah32 with regulator disabled)

Measure deep sleep current with instrument
(set range to 1A to avoid auto range disconnect)

Issues:
- 48mA ????
- Once wlan is on, current is high, regardless of setting active(False)
- How measure RTC connect time? Resets CPU timer.
- Add tests for wlan transmitting, receiving, and cpu busy

Results from tst.py:

2.39s for connecting to wlan

cpu on, wifi off                                 89mA        3.24V
cpu on, wifi off                                 91mA        3.25V
cpu on, wifi off                                 90mA        3.24V
cpu on, wlan active, no connection              154mA         3.2V
cpu on, wlan active, no connection              153mA         3.2V
cpu on, wlan active, no connection              153mA         3.2V
cpu on, wifi connected                          154mA         3.2V
cpu on, wifi connected                          154mA         3.2V
cpu on, wifi connected                          154mA         3.2V
cpu on, wifi connected                          154mA         3.2V
cpu on, wifi connected                          153mA         3.2V
cpu on, wifi connected                          152mA         3.2V
cpu on, wifi disconnected                       154mA        3.17V
cpu on, wifi disconnected                       154mA         3.2V
cpu on, wifi disconnected                       146mA         3.2V
cpu on, wlan inactive                           155mA         3.2V
cpu on, wlan inactive                           152mA         3.2V
cpu on, wlan inactive                           155mA         3.2V
deepsleep; reset to wake up                      48mA
