import network
import time
from webServer import WebServer
from neopixel import Neopixel
import uasyncio
import rp2

async def fill(colour):
    colour = hexCol2RGBCol(colour)
    leds.fill(colour)
    leds.show()

def showIP(ip):
    ip = ip.split(".")
    ip = int(ip[-1])

    colour = (255,255,0)
    for i in range(ip):
        leds.set_pixel(i,colour)
        leds.show()
        time.sleep(1)

def hex2rgb(hex):
    hexDigits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    first = hexDigits.index(hex[0:1]) * 16
    second = hexDigits.index(hex[1:2])

    return first + second

def hexCol2RGBCol(hex):
    return (hex2rgb(hex[0:2]),hex2rgb(hex[2:4]),hex2rgb(hex[4:6]))

rp2.PIO(0).remove_program()

methods = {"fill":(fill,["colour"])}

leds = Neopixel(50,0,0,"GRB")
leds.brightness(128)
leds.fill((0,0,0))
leds.show()

ssid = "TALKTALK0573C2_EXT"
password = "CNNHYFAW"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

    showIP(status[0])

    server = WebServer(methods,port=8350)
    uasyncio.run(server.start())
        
#start up, show IP
#multiple colours