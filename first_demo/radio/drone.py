# Add your Python code here. E.g.
from microbit import *
import radio

radio.on() # Radio won't work unless it's on
radio.config(channel=3)
incoming = 0


while True:
    incoming = str(radio.receive()) # Need to change to string for logic underneath.
    # https://www.geeksforgeeks.org/python-str-function/ 
    
    if (incoming != 0): # If a message is incoming
        display.scroll(incoming) # Display the incoming message
        split_string = incoming.split("_") # Split up the message wherever a "_" appear and add it to a list called split_string
        
        for x in range(len(split_string)): # Print each item in the list split_string
            display.scroll(split_string[x])

    
    
