import ibmiotf.application
import time
import json
try:
  configFilePath = "mqtt.cfg"
  options = ibmiotf.application.ParseConfigFile(configFilePath)
  client = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException as e:
  print(str(e))
  sys.exit()

print("(Press Ctrl+C to disconnect)")

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    evt = event.data
    t1rgb = evt['d']['tone1']['rgb']
    t1r = t1rgb[:3]
    t1g = t1rgb[3:-3]
    t1b = t1rgb[6:]
    print(t1r)
    print(t1g)
    print(t1b)
    
    #print(str % (event.format, event.event, event.device, json.dumps(event.data)))

client.connect()
#client.subscribeToDeviceEvents(deviceType="CognitiveLED", deviceId="b827eb416d4b", event="light")

#working for publish
#myData={'name': 'PC X','cpu':99,'mem':45}
#client.publishEvent("CognitiveLED", "b827eb416d4b", "status", "json", myData)

client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents()

while True:
  time.sleep(1)