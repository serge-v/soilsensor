import time
import tinypico as TinyPICO
from machine import SoftSPI, Pin, RTC
from dotstar import DotStar

RED = (128, 0, 0, 0.2)
GREEN = (0, 128, 0, 0.2)
BLUE = (0, 0, 128, 0.2)
YELLOW = (128, 128, 0, 0.2)
MAGENTA = (128, 0, 128, 0.2)

dotstar = None

def init():
    global dotstar
    spi = SoftSPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
    dotstar = DotStar(spi, 1, brightness = 0.5 )
    TinyPICO.set_dotstar_power(True)

def blink(n, color):
    for i in range(n):
        dotstar[0] = color
        time.sleep_ms(200)
        dotstar[0] = (0, 0, 0, 0)
        time.sleep_ms(200)
    time.sleep_ms(300)
