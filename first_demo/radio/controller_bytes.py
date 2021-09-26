# Add your Python code here. E.g.
from microbit import *
import radio

radio.on() # Radio won't work unless it's on
radio.config(channel=3)
pitch = 11


while True:
    message = "P_" + str(pitch)
    message_in_bytes = str.encode(message)
    radio.send_bytes(message_in_bytes)

