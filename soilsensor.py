import config
import time
from machine import SoftI2C, Pin

if config.Board == "tinys2":
    import tinys2 as tiny
else:
    import tinypico as tiny

import ustruct as struct

TOUCH_BASE = const(0x0F)
TOUCH_CHANNEL_OFFSET = const(0x10)
STATUS_BASE = const(0x00)
STATUS_SWRST = const(0x7F)
STATUS_HW_ID = const(0x01)
addr = const(0x36)

def get_moisture_internal():
    i2c = SoftI2C( scl=Pin(tiny.I2C_SCL), sda=Pin(tiny.I2C_SDA) )
    print(i2c.scan())

    # reset sensor
    buf = bytearray([STATUS_BASE, STATUS_SWRST, 0xFF])
    acks = i2c.writeto(addr, buf)
    time.sleep(0.5)

    # get hardware id
    buf = bytearray([STATUS_BASE, STATUS_HW_ID])
    acks = i2c.writeto(addr, buf)
    print("i2c.write (hw_id):", acks)
    time.sleep(0.008)
    resp = bytearray(1)
    i2c.readfrom_into(addr, buf)
    print("hw_id: {:x}".format(buf[0]))

    # read moisture up to 5 times:

    moisture = 0

    for i in range(5):
        buf = bytearray([TOUCH_BASE, TOUCH_CHANNEL_OFFSET])
        acks = i2c.writeto(addr, buf)
        print("i2c.write:", acks)
        time.sleep(0.008)
        resp = bytearray(2)
        i2c.readfrom_into(addr, resp)
        moisture = struct.unpack(">H", resp)[0]
        print("moisture:", moisture)
        time.sleep(0.5)
        if moisture >= 200 and moisture <= 2000:
            break

    return moisture

def get_moisture():
    try:
        return get_moisture_internal()
    except OSError as err:
        print(err)
        return 0
