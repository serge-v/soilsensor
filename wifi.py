import config
import network, time
import usocket as socket
import ussl as ssl

if config.Board == "tinys2":
    import tinys2 as tiny
else:
    import tinypico as tiny

import blink

def send_msg_raw(msg):
    blink.blink(1, blink.BLUE)

    addr = socket.getaddrinfo(config.Host, 443)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s = ssl.wrap_socket(s, server_hostname=config.Host)
    
    req = b'GET /log/?m=' + msg + '&f=' + config.Name + ' HTTP/1.1\r\nHost: ' + config.Host + '\r\n\r\n'
    s.write(req)

    data = s.read(12)
    print(data)

    s.close()
    blink.blink(2, blink.BLUE)

def send_msg(msg):
    try:
        send_msg_raw(msg)
    except OSError as err:
        print("error:", err)
        blink.blink(3, blink.RED)

def connect():
    wlan = network.WLAN(network.STA_IF)
    attempts = 3
    while attempts > 0:
        try:
            blink.blink(1, blink.GREEN)
            wlan.active(True)
            time.sleep(1)
            wlan.connect(config.SSID, config.Password)
            time.sleep(5)
            if wlan.isconnected():
                blink.blink(1, blink.GREEN)
                return
        except OSError as err:
            wlan.active(False)
            print("error:", err)
            blink.blink(3, blink.RED)
            time.sleep(4)
        except:
            print("unknown error")
            raise
        print("next attempt", attempts)
        attempts -= 1
    blink.blink(5, blink.RED)
    print("go sleep after 3 attempts")
    tiny.go_deepsleep(60000)
