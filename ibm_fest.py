import sys
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
import ibmiotf.application
import time
import json
import time
import random
from neopixel import *
import argparse
import math

# LED strip configuration:
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 3       # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# MQTT function
def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    evt = event.data
    global tones
    global newtone
    newtone = True
    tones = None
    tones = {
        "tone1": evt['d']['tone1'],
        "tone2": evt['d']['tone2'],
        "tone3": evt['d']['tone3']
    }
    print (tones)

# Define functions which animate LEDs in various ways.
def colorWipe(wait_ms=25):
    """Wipe color across display a pixel at a time."""
    #print("colorwipe:" + str(color))
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]
    for i in range(1, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(1,strip.numPixels()):
        strip.setPixelColor(i, Color(t1r,t1g,t1b))
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorZero(wait_ms=25):
    for i in range(1,strip.numPixels()):
        strip.setPixelColor(i,Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, Color(t1r,t1g,t1b))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def scale(color, k):
    r0 = min(color[0]*k, 255)
    g0 = min(color[1]*k, 255)
    b0 = min(color[2]*k, 255)

    return (r0, g0, b0)

def sparkle():
    p = speed / 100
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]

    for i in range(strip.numPixels()):
        srgb = scale(tones[random.choice(list(tones.keys()))]['rgb'],random.randrange(0,p)==0)
        if srgb[0] == 0 and srgb[1] == 0 and srgb[2] == 0:
            strip.setPixelColor(i, Color(t1r,t1g,t1b))
        else:
            strip.setPixelColor(i, Color(srgb[0],srgb[1],srgb[2]))

    strip.show()
    time.sleep(random.uniform(0.05,0.15))

def fireeffect():
    rgb = tones['tone1']['rgb']
    for i in range(strip.numPixels()):
        flicker = random.randrange(0,255)

        r1 = rgb[0] - flicker
        g1 = rgb[1] - flicker
        b1 = rgb[2] - flicker

        if g1 < 0:
            g1 = 0
        if r1 < 0:
            r1=0
        if b1 < 0:
            b1=0
        strip.setPixelColor(i, Color(r1,g1,b1))

    strip.show()
    time.sleep(random.uniform(0.05,0.15))

def millis():
    return time.time()

def duration(start):
    return millis() - start

def getStepFloat(t0, t, v):
    return (((duration(start)-t0)%t)*v/t)

def interpolate(j0, j1, x):
    r0 = x*(tones[list(tones.keys())[j1]]['rgb'][0] - tones[list(tones.keys())[j0]]['rgb'][0]) + tones[list(tones.keys())[j0]]['rgb'][0]
    g0 = x*(tones[list(tones.keys())[j1]]['rgb'][1] - tones[list(tones.keys())[j0]]['rgb'][1]) + tones[list(tones.keys())[j0]]['rgb'][1]
    b0 = x*(tones[list(tones.keys())[j1]]['rgb'][2] - tones[list(tones.keys())[j0]]['rgb'][2]) + tones[list(tones.keys())[j0]]['rgb'][2]
    return (r0, g0, b0)

def constrain(val, min_val, max_val):
    if val < min_val: return min_val
    if val > max_val: return max_val
    return val

def getPalColor(i):
    i0 = int(i%(len(tones)))
    i1 = int((i+1)%(len(tones)))
    t0 = i - math.trunc(i)

    return (interpolate(i0, i0, t0))

def comet():
    devtime = duration(start) * 500
    l = strip.numPixels()/2;  #length of the tail
    t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    tx = getStepFloat(devtime, speed, len(tones))
    c = getPalColor(tx)

    for i in range(strip.numPixels()):
        if (i-t) < 0:
            x = 1
        else:
            x = 0
        k = constrain( (((i-t)/l+1.2))*(x), 0, 1)
        clr = scale(c, k)
        strip.setPixelColor(i, Color(int(clr[0]),int(clr[1]),int(clr[2])))

    strip.show()
    time.sleep(random.uniform(0.05,0.15))    

# Main program logic follows:
if __name__ == '__main__':
    try:
        start = millis()
        configFilePath = "mqtt.cfg"
        options = ibmiotf.application.ParseConfigFile(configFilePath)
        client = ibmiotf.application.Client(options)
    except ibmiotf.ConnectionException as e:
        print(str(e))
        sys.exit()

    AnimationSeq = [
        "sparkle",
        "comet",
        "colorWipe"
    ]

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')

    # MQTT connect
    client.connect()

    client.deviceEventCallback = myEventCallback
    client.subscribeToDeviceEvents()

    tones = None
    newtone = False
    speed = 3000
    effect = ''

    print (tones)
    print (newtone)

    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            if tones:
                if newtone:
                    newtone = False
                    effect = AnimationSeq[random.randrange(0,len(AnimationSeq))]
                    exec(effect + '()')
                else:
                    exec(effect + '()')
            else:
                time.sleep(random.uniform(0.05,0.15)) 

    except KeyboardInterrupt:
        colorZero()