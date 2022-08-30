import config

if config.Board == "tinys2":
    import tinys2 as tiny
    from neopixel import NeoPixel
elif config.Board == "tinys3":
    import tinys3 as tiny
    from neopixel import NeoPixel
else:
    import tinypico as TinyPICO
    from dotstar import DotStar

import time
from machine import SoftSPI, Pin, RTC

RED = (128, 0, 0, 0.2)
GREEN = (0, 128, 0, 0.2)
BLUE = (0, 0, 128, 0.2)
YELLOW = (128, 128, 0, 0.2)
MAGENTA = (128, 0, 128, 0.2)

blinker = None

def initDotstar():
    global blinker
    spi = SoftSPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
    blinker = DotStar(spi, 1, brightness = 0.5 )
    TinyPICO.set_dotstar_power(True)

def initNeopixel():
    global blinker
    blinker = NeoPixel(Pin(tiny.RGB_DATA), 1)
    tiny.set_pixel_power(True)

def init():
    if config.Board == "tinys2" or config.Board == "tinys3":
        initNeopixel()
    else:
        initDotstar()
    
def blink(n, color):
    for i in range(n):
        blinker[0] = color
        if config.Board == "tinys2" or config.Board == "tinys3":
            blinker.write()
        time.sleep_ms(200)
        blinker[0] = (0, 0, 0, 0)
        if config.Board == "tinys2" or config.Board == "tinys3":
            blinker.write()
        time.sleep_ms(200)
    time.sleep_ms(300)
