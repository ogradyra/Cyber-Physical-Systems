from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
from micropython import *

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(channel=72) # A FEW PARAMETERS CAN BE SET BY THE PROGRAMMER
kbd_intr(-1)
# INITIALISE COMMANDS
# REMEMBER PARTY
pitch = 0
arm = 0
roll = 0
throttle = 0
yaw = 0

# NO NEED TO MAKE FUNCTIONS FOR THIS CONTROLLER
# JUST USE WHILE LOOP

prev_r = 0
prev_p = 0

def ledDisplay():
    if arm == 1:
        display.set_pixel(0,0,9)
    else:
        display.set_pixel(0,0,0)

while True:

	# INITIALISE COMMAND OUTPUT STRING
    command = ""

	# ARM THE DRONE USING BOTH BUTTONS
	# INCREASE THROTTLE WITH B BUTTON
	# CHECK OUT is_pressed() AND was_pressed() FUNCTIONS 
	# FIGURE OUT WHICH FUNCTION IS BETTER SUITED FOR THE CONTROLLER
            
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
        else:
            arm = 0
    
    if button_a.is_pressed():
        throttle -= 5
        
    if button_b.is_pressed():
        throttle += 5
            
    
    
    
	# USE ACCLEREROMETER CLASS FOR DEALING WITH ROLL, PITCH AND YAW (X, Y AND Z AXES)
	# FIND APPROPRIATE VALUES FOR EACH TO SEND ACROSS TO DRONE
	
    curr_r = accelerometer.get_x() # roll
    if prev_r > curr_r and roll > -45:
        roll -= 3
    elif curr_r > prev_r and roll < 45:
        roll +=3
    prev_r = curr_r
    
    curr_p = accelerometer.get_y() # pitch
    if prev_p > curr_p and pitch > -45:
        pitch -= 3
    elif curr_p > prev_p and pitch < 45:
        pitch +=3
    prev_p = curr_p
    
    #y = accelerometer.get_y() # pitch
    #z = accelerometer.get_z() # yaw
    #print(x)
    #print(y)
    #print(z)
    
    # shake command
    #if accelerometer.is_gesture("shake"):
        #arm = 0
    
    ledDisplay()
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    radio.send("P_" + str(pitch) + "_A_" + str(arm) + "_R_" + str(roll) + "_T_" + str(throttle))
    print("P_" + str(pitch) + "_A_" + str(arm) + "_R_" + str(roll) + "_T_" + str(throttle))
    #radio.send("Y" + str(yaw))
    
    sleep(100) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE
