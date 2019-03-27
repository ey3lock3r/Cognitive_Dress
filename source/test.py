import random
import time
import math

def scale(color, k):
    r0 = min(color[0]*k, 255)
    g0 = min(color[1]*k, 255)
    b0 = min(color[2]*k, 255)
    return (r0, g0, b0)

def sparkle():
    print('Sparkle')
    p = speed / 100   
    for i in range(100):
        color = scale(tones[random.choice(list(tones.keys()))],random.randrange(0,p)==0)
        if color[0] != 0 or color[1] != 0 or color[2] != 0:
            print(color)

def sparkle2():
    p = speed / 10
    #print(tones[random.choice(list(tones.keys()))]['rgb'])
    for i in range(100):
        if random.randint(0,p) == 0:
            srgb = tones[random.choice(list(tones.keys()))]
        else:
            srgb = scale(tones['tone1'],0.88)
        
        print(srgb)

def fireeffect():
    color = tones["tone1"]
    print('Fireeffect')
    for i in range(100):
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
        #print (tuple((r1, g1, b1)))
        #print (rgb1(r1, g1, b1))
    delay(random.randrange(50,150))
    #time.sleep(random.uniform(0.05,0.15))

def settones():
    global tones
    tones = {
        "tone1": (255,0,0),
        "tone2": (0,255,0),
        "tone3": (0,0,255)
    }

def millis():
    return time.time() * 1000

def duration(start):
    return millis() - start

def getStepFloat(t0, t, v):
    #call millis func at start
    return (((duration(start)-t0)%t)*v/t)

def interpolate(tones, j0, j1, x):
    # convert to int?
    #tt = tones.keys(j0)     
    #r0 = x*(tones.keys()[j1]['rgb'][0] - tones.keys()[j0]['rgb'][0]) + tones.keys()[j0]['rgb'][0]
    #print(tones[list(tones.keys())[0]][0])

    r0 = x*(tones[list(tones.keys())[j1]][0] - tones[list(tones.keys())[j0]][0]) + tones[list(tones.keys())[j0]][0]
    g0 = x*(tones[list(tones.keys())[j1]][1] - tones[list(tones.keys())[j0]][1]) + tones[list(tones.keys())[j0]][1]
    b0 = x*(tones[list(tones.keys())[j1]][2] - tones[list(tones.keys())[j0]][2]) + tones[list(tones.keys())[j0]][2]
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
    
    return (interpolate(tones, i0, i1, t0))

def comet():
    # start = millis() put at the beginning of program
    devtime = duration(start)
    devtime = start + 10000000
    #print('Comet')
    #l = strip.numPixels()/2;  #length of the tail
    l = strip/2;  #length of the tail
    #t = getStepFloat(devtime, speed, 2*strip.numPixels()-l)
    t = getStepFloat(devtime, speed, 2*strip-l)
    tx = getStepFloat(devtime, speed, len(tones))
    c = getPalColor(tx, tones)
    print(t)
    print(tx)
    print(c)

    for i in range(100):
        if (i-t) < 0:
            x = 1
        else:
            x = 0
        k = constrain( (((i-t)/l+1.2))*(x), 0, 1)
        color = scale(c, k)
        if color[0] == 0 and color[1] == 0 and color[2] == 0:
            color = tones['tone1']
        print(color)

def sum(tones, j0, j1):
    r0 = min(tones[list(tones.keys())[j0]][0] + tones[list(tones.keys())[j1]][0], 255)
    g0 = min(tones[list(tones.keys())[j0]][1] + tones[list(tones.keys())[j1]][1], 255)
    b0 = min(tones[list(tones.keys())[j0]][2] + tones[list(tones.keys())[j1]][2], 255)
    return (r0, g0, b0)

def mapfloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def bouncingBalls():
    #global lastRefresh
    print(pxPos[0])
    print(pxPos[1])
    print(pxPos[2])
    if pxPos[0] == 0 and pxPos[1] == 0 and pxPos[2] == 0:
        # allocate new arrays
        for i in range(0, len(tones)):
            #pxPos[i] = ((float)random(255))/255
            pxPos[i] = tones[list(tones.keys())[i]]
            pxSpeed[i] = 0
        lastRefresh = millis()
        print ("First run")
        return # skip the first cycle

    print('Succeeding runs')
    speedReduction = (millis() - lastRefresh)/5000
    lastRefresh = millis()

    pxPos = pxPos + pxSpeed
    for i in range(0, len(tones)):
        if pxSpeed[i]>-0.04 and pxSpeed[i]<0 and pxPos[i]>0 and pxPos[i]<0.1:
            pxSpeed[i]=(0.09)-(random.uniform(0,10)/1000)

        #pxPos[i] = pxPos[i] + pxSpeed[i]
        if pxPos[i] >= 1:
            pxPos[i] = 1

        if pxPos[i] < 0:
            pxPos[i] = pxPos[i] - pxPos[i]
            pxSpeed[i] = pxSpeed[i]- 0.91 * pxSpeed[i]

        pxSpeed[i] = pxSpeed[i] - speedReduction

    #for i in range(strip.numPixels()):
        #strip.setPixelColor(i, Color(0,0,0))

    for i in range(0, len(tones)):
        p = mapfloat(pxPos[i], 0, 1, 0, strip.numPixels() - 1)
        print(i + ": " + sum(tones, 0, i))
        #strip.setPixelColor(p, Color(sum(tones, 0, i)))
    
    #strip.show()
    time.sleep(random.uniform(0.05,0.15))

AnimationSeq = [
    "sparkle",
    "fireeffect",
    "comet"
]

strip = 60
speed = 1000
start = millis()
pxPos = [0,0,0]
pxSpeed = [0.0,0.0,0.0]
lastRefresh = 0
settones()
#for i in len(tones):
for i in range(0,100):
    #comet()
    bouncingBalls()
#print(AnimationSeq[random.randrange(0,len(AnimationSeq))]+'()')
#exec(AnimationSeq[random.randrange(0,len(AnimationSeq))]+'()')
#exec(AnimationSeq['random.randrange(0,len(AnimationSeq))']+'(tones["tone1"])')

#print (start)
#fireeffect(tones["tone1"])
#sparkle(tones,1000)
#comet(60, tones, 1000)