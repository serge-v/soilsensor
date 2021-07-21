import machine
import time
import esp32
import tinypico as TinyPICO
from machine import RTC, WDT

from micropython import const

import blink, wifi, soilsensor

wdt = WDT(timeout=30000)
wdt.feed()

print("blink.init")
blink.init()

reset = machine.reset_cause()

if reset == machine.DEEPSLEEP_RESET:
    blink.blink(1, blink.MAGENTA)
    print("deepsleep reset")
elif reset == machine.WDT_RESET:
    blink.blink(3, blink.MAGENTA)
    print("watchdog reset")
else:
    blink.blink(reset, blink.RED)

print("reset cause:", machine.reset_cause())

moisture = soilsensor.get_moisture()

print("wifi.connect")
wifi.connect()

blink.blink(3, blink.GREEN)

time.sleep(2)

rtc = RTC()
ts = rtc.datetime()
volts = TinyPICO.get_battery_voltage()

msg = '{:04}-{:02}-{:02}+{:02}:{:02}:{:02}'.format(ts[0], ts[1], ts[2], ts[4], ts[5], ts[6])
msg += "+reset:{}+t:{}F+hall:{}".format(reset, esp32.raw_temperature(), esp32.hall_sensor())
msg += "+batv:{:.2f}V".format(volts)
msg += "+moisture:{}".format(moisture)

print("sending:", msg)
wifi.send_msg(msg)

TinyPICO.go_deepsleep(60000)
