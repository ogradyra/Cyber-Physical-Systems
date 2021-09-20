# Add your Python code here. E.g.
from microbit import *
import radio

radio.on() # Radio won't work unless it's on
radio.config(channel=3)
incoming = 0


while True:
    incoming = str(radio.receive())
    
    if (incoming != 0):
        display.scroll(incoming)
