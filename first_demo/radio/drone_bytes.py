# Add your Python code here. E.g.
from microbit import *
import radio

radio.on() # Radio won't work unless it's on
radio.config(channel=3)
incoming = 0



while True:
    incoming = radio.receive_bytes()
    split_byte_list = []
    if (incoming !=  None): # If a message is incoming
        display.scroll("In")
        print(str(incoming))
        print(len(incoming))
        split_byte_list = [incoming[i] for i in range (0, len(incoming))]
        for x in split_byte_list:
            print(x)
