#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

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
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# MQTT function
def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    evt = event.data
    global tones
    global newtone
    newtone = True
    tones = {
        "tone1": evt['d']['tone1'],
        "tone2": evt['d']['tone2'],
        "tone3": evt['d']['tone3']
    }
    print (tones)
    #tones['tone1']['rgb'][0] = int(round(tones['tone1']['rgb'][0] * tones['tone1']['intensity']))
    #tones['tone1']['rgb'][1] = int(round(tones['tone1']['rgb'][1] * tones['tone1']['intensity']))
    #tones['tone1']['rgb'][2] = int(round(tones['tone1']['rgb'][2] * tones['tone1']['intensity']))
    #t1r = tones['tone1']['rgb'][0]
    #t1g = tones['tone1']['rgb'][1]
    #t1b = tones['tone1']['rgb'][2]
    #print(t1r)
    #print(t1g)
    #print(t1b)
    #print(str % (event.format, event.event, event.device, json.dumps(event.data)))
    #print ('Event Callback Color wipe animation.')
    #colorWipe(strip, Color(0,0,0))  # Red wipe
    #print ('Color sparkle animations.')
    #sparkle(strip, tones, 1000)
    #while True:
        #fireeffect(strip, tones['tone1']['rgb'])
        #comet(strip, tones, 1000)
    #print ('Theater chase animations.')
    #theaterChase(strip, Color(127, 127, 127))  # White theater chase
    #theaterChase(strip, Color(t1r, t1g, t1b))  # Red theater chase
    #theaterChase(strip, Color(t2r, t2g, t2b))  # Red theater
    #theaterChase(strip, Color(t3r, t3g, t3b))  # Red theater
    #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
    #print ('Rainbow animations.')
    #rainbow(strip)
    #rainbowCycle(strip)
    #theaterChaseRainbow(strip)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

#sleep takes seconds
#delay takes milisec
def scale(color, k):
    #print(color)
    #print(k)
    r0 = min(color[0]*k, 255)
    g0 = min(color[1]*k, 255)
    b0 = min(color[2]*k, 255)
    #print(r0)
    #print(g0)
    #print(b0)
    return (r0, g0, b0)

def sparkle():
    p = speed / 100
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]
    #print(tones[random.choice(list(tones.keys()))]['rgb'])
    for i in range(strip.numPixels()):
        srgb = scale(tones[random.choice(list(tones.keys()))]['rgb'],random.randint(0,p)==0)
        if srgb[0] == 0 and srgb[1] == 0 and srgb[2] == 0:
            strip.setPixelColor(i, Color(t1r,t1g,t1b))
        else:
            strip.setPixelColor(i, Color(srgb[0],srgb[1],srgb[2]))
    strip.show()
    time.sleep(random.uniform(0.05,0.15))

def sparkle2():
    p = speed / 10

    #print(tones[random.choice(list(tones.keys()))]['rgb'])
    for i in range(strip.numPixels()):
        if random.randint(0,p) == 0:
            srgb = tones[random.choice(list(tones.keys()))]['rgb']
        else:
            srgb = scale(tones['tone1']['rgb'],0.88)
        
        strip.setPixelColor(i, Color(srgb[0],srgb[1],srgb[2]))
    
    strip.show()
    time.sleep(random.uniform(0.05,0.15))

def fireeffect():
    #print (rgb)
    rgb = tones['tone1']['rgb']
    for i in range(strip.numPixels()):
        flicker = random.randrange(0,255)
        #print(flicker)
        #flicker = random.randint(0,40)
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
    #delay(random.randrange(50,150))
    time.sleep(random.uniform(0.05,0.15))

def millis():
    return time.time()

def duration(start):
    return millis() - start

def getStepFloat(t0, t, v):
    #call millis func at start
    return (((duration(start)-t0)%t)*v/t)

def mapfloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def interpolate(tones, j0, j1, x):
    # convert to int?
    #tt = tones.keys(j0)     
    #r0 = x*(tones.keys()[j1]['rgb'][0] - tones.keys()[j0]['rgb'][0]) + tones.keys()[j0]['rgb'][0]
    #print(tones[list(tones.keys())[0]][0])

    r0 = x*(tones[list(tones.keys())[j1]]['rgb'][0] - tones[list(tones.keys())[j0]]['rgb'][0]) + tones[list(tones.keys())[j0]]['rgb'][0]
    g0 = x*(tones[list(tones.keys())[j1]]['rgb'][1] - tones[list(tones.keys())[j0]]['rgb'][1]) + tones[list(tones.keys())[j0]]['rgb'][1]
    b0 = x*(tones[list(tones.keys())[j1]]['rgb'][2] - tones[list(tones.keys())[j0]]['rgb'][2]) + tones[list(tones.keys())[j0]]['rgb'][2]
    return (r0, g0, b0)

def constrain(val, min_val, max_val):
    if val < min_val: return min_val
    if val > max_val: return max_val
    return val

def getPalColor(i, tones):
    i0 = int(i%(len(tones)))
    i1 = int((i+1)%(len(tones)))

    #decimal part is used to interpolate between the two colors
    #import math
    t0 = i - math.trunc(i)
    #float t0 = i - (int)i;
    
    return (interpolate(tones, i0, i0, t0))

def comet():
    # start = millis() put at the beginning of program
    devtime = duration(start) * 500
    #print (start)
    #print (devtime)

    #l = strip.numPixels()/2;  #length of the tail
    l = strip.numPixels()/2;  #length of the tail
    #t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    tx = getStepFloat(devtime, speed, len(tones))
    c = getPalColor(tx, tones)

    for i in range(strip.numPixels()):
        if (i-t) < 0:
            x = 1
        else:
            x = 0
        k = constrain( (((i-t)/l+1.2))*(x), 0, 1)
        clr = scale(c, k)
        #print(clr)
        strip.setPixelColor(i, Color(int(clr[0]),int(clr[1]),int(clr[2])))
        
    strip.show()
    time.sleep(random.uniform(0.05,0.15))    

def comet2():
    # start = millis() put at the beginning of program
    devtime = duration(start) * 500
    #print (start)
    #print (devtime)

    #l = strip.numPixels()/2;  #length of the tail
    l = strip.numPixels()/2;  #length of the tail
    #t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    tx = getStepFloat(devtime, speed, len(tones))
    c = getPalColor(tx, tones)

    for i in range(strip.numPixels()):
        if (i-t) < 0:
            x = 1
        else:
            x = 0
        k = constrain( (((i-t)/l+1.2))*(x), 0, 1)
        clr = scale(c, k)
        #print(clr)
        strip.setPixelColor(i, Color(int(clr[0]),int(clr[1]),int(clr[2])))
    strip.show()
    time.sleep(random.uniform(0.05,0.15))    

def sum(tones, j0, j1):
    r0 = min(tones[list(tones.keys())[j0]]['rgb'][0] + tones[list(tones.keys())[j1]]['rgb'][0], 255)
    g0 = min(tones[list(tones.keys())[j0]]['rgb'][1] + tones[list(tones.keys())[j1]]['rgb'][1], 255)
    b0 = min(tones[list(tones.keys())[j0]]['rgb'][2] + tones[list(tones.keys())[j1]]['rgb'][2], 255)
    return (r0, g0, b0)

def bouncingBalls():
    if pxPos==None:
        # allocate new arrays

        for i in range(0, len(tones)):
            #pxPos[i] = ((float)random(255))/255
            pxPos[i] = tones[list(tones.keys())[i]]['rgb'][i]
            pxSpeed[i] = 0

        lastRefresh = millis()

        return # skip the first cycle

    speedReduction = (millis() - lastRefresh)/5000
    lastRefresh = millis()

    for i in range(0, len(tones)):
        if pxSpeed[i]>-0.04 and pxSpeed[i]<0 and pxPos[i]>0 and pxPos[i]<0.1:
            pxSpeed[i]=(0.09)-(random.uniform(0,10)/1000)

        pxPos[i] = pxPos[i] + pxSpeed[i]
        if pxPos[i] >= 1:
            pxPos[i] = 1

        if pxPos[i] < 0:
            pxPos[i] = pxPos[i] - pxPos[i]
            pxSpeed[i] = pxSpeed[i]- 0.91 * pxSpeed[i]

        pxSpeed[i] = pxSpeed[i] - speedReduction

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))

    for i in range(0, len(tones)):
        p = mapfloat(pxPos[i], 0, 1, 0, strip.numPixels() - 1)
        strip.setPixelColor(p, Color(sum(tones, 0, i)))
    
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
        "sparkle2",
        "fireeffect",
        "comet"
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

    lastRefresh = 0
    pxPos = None
    pxSpeed = None
    tones = None
    newtone = False
    speed = 1000
    effect = ''

    print (tones)
    print (newtone)

    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            if tones:
                #print ('Tone is not null')
                if newtone:
                    #print ('newTone is true')
                    #effect = random.randrange()
                    newtone = False
                    lastRefresh = 0
                    effect = AnimationSeq[random.randrange(0,len(AnimationSeq))]
                    exec(effect + '()')
                    #print ('Sparkle effect')
                    #sparkle(strip, tones, 1000)
                else:
                    #runanimation(effect)
                    #print ('Sparkle effect')
                    #sparkle(strip, tones, 1000)
                    #print ('Fire effect')
                    exec(effect + '()')
                    #print ('Comet')
                    #comet(strip, tones, 1000)
            else:
                time.sleep(1)
                #print ('Tone is null')
            #time.sleep(1)
            #print(str % (event.format, event.event, event.device, json.dumps(event.data)))
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(0, 0, 0))  # Red wipe
            #print ('Color wipe animations.')
            #colorWipe(strip, tones['tone1']['rgb'])
            #print ('Color sparkle animations.')
            #sparkle(strip, tones, 1000)
            #print ('Color sparkle animations.')
            #sparkle(strip, tones, 1000)
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)
    except KeyboardInterrupt:
        #if args.clear:
        colorWipe(strip, Color(0,0,0), 10)