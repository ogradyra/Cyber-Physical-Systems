# Add your Python code here. E.g.
from microbit import *
import radio
import micropython

radio.on()
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)

while True:
    incoming = radio.receive()
    
    if incoming:
        string = incoming.split(",")
        address = int(string[0])
        if address == 2:
            pitch = int(string[1])
            roll  = int(string[2])
            print("Pitch: ", pitch, " Roll: ", roll)
    
    sleep(100)
    
