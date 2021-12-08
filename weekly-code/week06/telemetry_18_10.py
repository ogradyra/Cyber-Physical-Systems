from microbit import *
import radio

radio.on()
radio.config(channel=47)
incoming = 0


while True:
    incoming = str(radio.receive())
    
    if incoming:
        if incoming[1] != "_":
            print(incoming)
        sleep(50)
