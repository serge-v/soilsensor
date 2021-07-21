# soilsensor
WiFi soil moisture data logger using TinyPICO and Adafruit I2C Capacitive Moisture Sensor.

On reset sends moisture data to the https://[config.Host]/log endpoint then goes to deep sleep for one minute.

## Configuration
Create config.py file:

    SSID = 'WiFi SSID name'
    Password = 'WiFi password'
    Host = 'Logger hostname'
 
 ## Upload
 Install rshell and run `./upload` to upload sensor program to the device.

## LED blinking

    Magenta, 1 time  -- DEEPSLEEP_RESET. Main work mode.
    Magenta, 3 times -- WDT_RESET. Means unhandled exception somewhere.
    Red, 1 time      -- PWRON_RESET
    Red, 2 times     -- HARD_RESET
    Red, 5 times     -- SOFT_RESET. Reset button was hit.

    Green, 1 times   -- start connecting to WiFi.
    Green, 3 times   -- connected to WiFi.
    Blue, 1 time     -- start sending to [Host].
    Blue, 2 times    -- message sent successfully.

## Message format

soilsensor makes `GET /log/?m=message` request to the configured host.
Message format is Timestamp followed by list of Key:Value pairs separated by space (escaped as a plus sign).

Message example:

    2000-01-01+00:00:13+reset:1+t:117F+hall:21+batv:3.70V+moisture:333

Fields:

- Timestamp as 2006-01-02 15:04:05 in UTC.
- reset reason
- temperature (F)
- hall sensor value
- battery voltage (3.7V - max)
- moisture (200 - min, 2000 - max)

