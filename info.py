import tinypico as TinyPICO
from machine import RTC
import micropython

def info():
    print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
    print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()

    rtc = RTC()
    print("rtc: {}".format(rtc.datetime()))
