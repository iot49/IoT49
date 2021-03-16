from machine import RTC

rtc = RTC()
rtc.ntp_sync(server="hr.pool.ntp.org")
