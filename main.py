import network
import time
from webServer import WebServer
from neopixel import Neopixel

leds = Neopixel(50,0,0,"GRB")
color = (255,255,0)
leds.fill(color,50)
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

    # server = WebServer({},port=8350)
    # server.start()
        
        