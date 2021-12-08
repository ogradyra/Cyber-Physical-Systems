from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

arm = 0


while True:
   
    	# ARM COMMAND
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
        else:
            arm = 0
    
    
    pitch = 512
    roll = 521
    
    #print("Pitch: ", pitch, "|", "Roll: ", roll)
    
    radio.send("P_" + str(pitch) + "_A_" + str(arm) + "_R_" + str(roll) + "_T_" + str(r_up))
