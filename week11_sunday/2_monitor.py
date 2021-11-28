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
        #print(string)
        address = int(string[0])
        if address == 2:
            if string[1] == '0':
                pitch = int(string[2])
                roll  = int(string[3])
                #print("Pitch: ", pitch, " Roll: ", roll)
                radio.send("0" + "," + "1" + "," + "1")
                sleep(3000)
                
                
                
'''     else:
                radio.send("0"+ "," + "1" + "," + "0")
        else:
            radio.send("0" + "," + "1" + "," + "0")'''
