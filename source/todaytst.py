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
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50       # Set to 0 for darkest and 255 for brightest
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
    t1r = tones['tone1']['rgb'][1]
    t1g = tones['tone1']['rgb'][0]
    t1b = tones['tone1']['rgb'][2]
    for i in range(1, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)
    time.sleep(2)
    for i in range(1,strip.numPixels()):
        strip.setPixelColor(i, Color(t1r,t1g,t1b))
        strip.show()
        time.sleep(wait_ms/1000.0)
    time.sleep(5)

def colorPie(wait_ms=25):
    """Wipe color across display a pixel at a time."""
    tot_weight = tones['tone1']['intensity'] + tones['tone2']['intensity'] + tones['tone3']['intensity']
    t1_ratio = round(tones['tone1']['intensity']/tot_weight*LED_COUNT)
    t2_ratio = round(tones['tone2']['intensity']/tot_weight*LED_COUNT) + t1_ratio
    t3_ratio = round(tones['tone3']['intensity']/tot_weight*LED_COUNT) + t2_ratio
    for i in range(1, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)
    time.sleep(2)
    for i in range(1,strip.numPixels()):
        if i <= t1_ratio:
            strip.setPixelColor(i, Color(tones['tone1']['rgb'][0],tones['tone1']['rgb'][1],tones['tone1']['rgb'][2]))
        elif i <= t2_ratio:
            strip.setPixelColor(i, Color(tones['tone2']['rgb'][0],tones['tone2']['rgb'][1],tones['tone2']['rgb'][2]))
        else:
            strip.setPixelColor(i, Color(tones['tone3']['rgb'][0],tones['tone3']['rgb'][1],tones['tone3']['rgb'][2]))
        strip.show()
        time.sleep(wait_ms/1000.0)
    time.sleep(5)

def colorZero(wait_ms=25):
    for i in range(1,strip.numPixels()):
        strip.setPixelColor(i,Color(0,0,0))
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
    p = speed / 300
    t1r = tones['tone1']['rgb'][1]
    t1g = tones['tone1']['rgb'][0]
    t1b = tones['tone1']['rgb'][2]
    #print(tones[random.choice(list(tones.keys()))]['rgb'])
    for i in range(strip.numPixels()):
        srgb = scale(tones[random.choice(list(tones.keys()))]['rgb'],random.randrange(0,p)==0)
        if srgb[0] == 0 and srgb[1] == 0 and srgb[2] == 0:
            strip.setPixelColor(i, Color(t1r,t1g,t1b))
        else:
            strip.setPixelColor(i, Color(srgb[0],srgb[1],srgb[2]))
    strip.show()
    time.sleep(random.uniform(0.05,0.15))
    for i in range(1,strip.numPixels()):
        strip.setPixelColor(i, Color(t1r,t1g,t1b))
    strip.show()
    time.sleep(1)

def millis():
    return time.time()

def duration(start):
    return millis() - start

def getStepFloat(t0, t, v):
    #call millis func at start
    return (((duration(start)-t0)%t)*v/t)

def interpolate(j0, j1, x):
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

def getPalColor(i):
    i0 = int(i%(len(tones)))
    i1 = int((i+1)%(len(tones)))

    #decimal part is used to interpolate between the two colors
    #import math
    t0 = i - math.trunc(i)
    #float t0 = i - (int)i;
    
    #if tones['tone1']['intensity'] >= 0.5:
    #    return (interpolate(i0, i1, t0))
    #else:
    #    return (interpolate(i0, i0, t0))
    return (interpolate(i0, i0, t0))

def comet():
    global start 
    # start = millis() put at the beginning of program
    devtime = duration(start) * 300 #500
    #print (start)
    #print (devtime)
    off = True

    #l = strip.numPixels()/2;  #length of the tail
    l = strip.numPixels()/3  #length of the tail
    #t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    tx = getStepFloat(devtime, speed, len(tones))
    c = getPalColor(tx)

    for i in range(strip.numPixels()):
        if (i-t) < 0:
            x = 1
        else:
            x = 0
        k = constrain( (((i-t)/l+1.2))*(x), 0, 1)
        if k != 0:
            off = False
        clr = scale(c, k)
        #print ("i",i," x",x," k",k)
        strip.setPixelColor(i, Color(int(clr[0]),int(clr[1]),int(clr[2])))

    strip.show()
    time.sleep(random.uniform(0.15,0.25))  
    if off:
        start = millis()
        time.sleep(3)

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

    transEffect = [
        "colorWipe",
        "theaterChase",
        "rainbow",
        "rainbowCycle",
        "theaterChaseRainbow"
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
                #print ('Tone is not null')
                if newtone:
                    t1r = tones['tone1']['rgb'][0]
                    t1g = tones['tone1']['rgb'][1]
                    t1b = tones['tone1']['rgb'][2]
                    #colorWipe(strip, Color(t1r,t1g,t1b))
                    newtone = False
                    #effect = AnimationSeq[random.randrange(0,len(AnimationSeq))]
                    effect = "sparkle"
                    exec(effect + '()')
                    #sparkle()
                else:
                    exec(effect + '()')
            else:
                time.sleep(1) 

    except KeyboardInterrupt:
        #if args.clear:
        colorZero()