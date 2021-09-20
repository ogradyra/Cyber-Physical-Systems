# Add your Python code here. E.g.
from microbit import *
import radio

radio.on() # Radio won't work unless it's on
radio.config(channel=3)


while True:
    message = 'Hello World'
    radio.send(message)
    display.scroll(message)
