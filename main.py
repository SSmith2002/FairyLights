import network
import time
from webServer import WebServer
from neopixel import Neopixel
import uasyncio
import rp2
import random

async def gradient(colour1,colour2):
    global currPixels
    global active

    active += 1
    while(active > 1):
        await uasyncio.sleep_ms(animationSpeed)

    colour1,colour2 = hexCol2RGBCol(colour1),hexCol2RGBCol(colour2)
    r = colour1[0]
    g = colour1[1]
    b = colour1[2]
    rD = round((colour1[0] - colour2[0]) / 50)
    gD = round((colour1[1] - colour2[1]) / 50)
    bD = round((colour1[2] - colour2[2]) / 50)

    for i in range(50):
        colour = (r,g,b)
        leds.set_pixel(i,colour)
        
        r += rD
        g += gD
        b += bD

        currPixels[i] = colour
    leds.show()

    active -= 1

async def fillBlock(colour):
    global currPixels
    global active

    active += 1
    while(active > 1):
        await uasyncio.sleep_ms(animationSpeed)
    
    colour = hexCol2RGBCol(colour)
    for i in range(50):
        leds.set_pixel(i,colour)
        currPixels[i] = colour
    leds.show()

    active -= 1

async def fillPattern(colour):
    global currPixels
    global active

    active += 1
    while(active > 1):
        await uasyncio.sleep_ms(animationSpeed)
    
    colour = hexCol2RGBCol(colour)

    while(active == 1):
        for i in range(50):
            newCol = (random.randint(0,colour[0]),random.randint(0,colour[1]),random.randint(0,colour[2]))
            leds.set_pixel(i,newCol)
            currPixels[i] = newCol
        leds.show()
        await uasyncio.sleep_ms(animationSpeed)

    active -= 1

async def fillPatternCol(colour):
    global currPixels
    global active

    active += 1
    while(active > 1):
        await uasyncio.sleep_ms(animationSpeed)
    
    colour = hexCol2RGBCol(colour)

    while(active == 1):
        for i in range(50):
            ratio = random.randint(0,255) / 255
            newCol = (round(colour[0]*ratio),round(colour[1]*ratio),round(colour[2]*ratio))
            leds.set_pixel(i,newCol)
            currPixels[i] = newCol
        leds.show()
        await uasyncio.sleep_ms(animationSpeed)

    active -= 1

def showIP(ip):
    global currPixels
    
    ip = ip.split(".")
    ip = int(ip[-1])

    colour = (255,255,0)
    for i in range(ip):
        leds.set_pixel(i,colour)
        currPixels[i] = colour
        leds.show()
        time.sleep(1)

async def updateBrightness(value):
    global currPixels
    value = int(value)
    leds.brightness(value)

    for i in range(len(currPixels)):
        leds.set_pixel(i,currPixels[i])
    leds.show()

async def updateSpeed(value):
    value = int(value)

    global animationSpeed
    if(value == 0):
        animationSpeed = 0
    else:
        animationSpeed = int((50 / value) *1000)

def hex2rgb(hex):
    hexDigits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    first = hexDigits.index(hex[0:1]) * 16
    second = hexDigits.index(hex[1:2])

    return first + second

def hexCol2RGBCol(hex):
    return (hex2rgb(hex[0:2]),hex2rgb(hex[2:4]),hex2rgb(hex[4:6]))

rp2.PIO(0).remove_program()
global animationSpeed
animationSpeed = int((50 / 50) * 1000)

global currPixels
currPixels = [(0,0,0) for i in range(50)]

global active
active = 0

methods = {"fillBlock":(fillBlock,["colour"]),
            "fillPattern":(fillPattern,["colour"]),
            "fillPatternCol":(fillPatternCol,["colour"]),
            "gradient":(gradient,["colour1","colour2"]),
            "updateBrightness":(updateBrightness,["value"]),
            "updateSpeed":(updateSpeed,["value"])}

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

#multiple colours
    #variable for pattern number
    # max of 5
    #pattern of 3 reveals 3 squares to colour
    #this pattern is then repeated

#flash all on then off
    #dynamic speed
    #variable to determine how wmany flash
        #1 - all flassh at same time
        #2 - every other flashes at same time
        #3 = every 3rd one in sequence etcgfh
    