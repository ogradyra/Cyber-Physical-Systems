from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=49)

display.off()

while True:
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()
    
    print("Pitch: ", pitch, "|", "Roll: ", roll)
