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
    tones = {
        "tone1": evt['d']['tone1'],
        "tone2": evt['d']['tone2'],
        "tone3": evt['d']['tone3']
    }
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]
    #print (tuple((tones['tone1']['rgb'])))
    print(str % (event.format, event.event, event.device, json.dumps(event.data)))
    print ('Event Callback Color wipe animation.')
    colorWipe(strip, Color(0,0,0))  # Red wipe
    while True: 
    	#print ('Color sparkle animations.')
    	sparkle(strip, tones, 1000)
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

def sparkle(strip, tones, speed):
    p = speed / 100
    t1r = tones['tone1']['rgb'][0]
    t1g = tones['tone1']['rgb'][1]
    t1b = tones['tone1']['rgb'][2]
    #print(tones[random.choice(list(tones.keys()))]['rgb'])
    for i in range(strip.numPixels()):
        srgb = scale(tones[random.choice(list(tones.keys()))]['rgb'],random.randrange(0,p)==0)
        print(srgb)
        #t2g = scale(tones[random.choice(list(tones.keys()))]['rgb'][1],random.randrange(0,p)==0)
        #t2b = scale(tones[random.choice(list(tones.keys()))]['rgb'][2],random.randrange(0,p)==0)
        if srgb[0] == 0 and srgb[1] == 0 and srgb[2] == 0:
            strip.setPixelColor(i, Color(t1r,t1g,t1b))
        else:
            strip.setPixelColor(i, Color(srgb[0],srgb[1],srgb[2]))
    strip.show()
    time.sleep(random.uniform(0.05,0.15))

def fireeffect(strip, color):
    for i in range(strip.numPixels()):
        flicker = random.randrange(0,41)
        #flicker = random.randint(0,40)
        r1 = color[0] - flicker
        g1 = color[1] - flicker
        b1 = color[2] - flicker

        if g1 < 0:
            g1 = 0
        if r1 < 0:
            r1=0
        if b1 < 0:
            b1=0
        strip.setPixelColor(i, tuple((r1,g1, b1)))

    strip.show()
    #delay(random.randrange(50,150))
    time.sleep(random.uniform(0.05,0.15))

# Main program logic follows:
if __name__ == '__main__':
    try:
        configFilePath = "mqtt.cfg"
        options = ibmiotf.application.ParseConfigFile(configFilePath)
        client = ibmiotf.application.Client(options)
    except ibmiotf.ConnectionException as e:
        print(str(e))
        sys.exit()

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

    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            time.sleep(1)

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
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)