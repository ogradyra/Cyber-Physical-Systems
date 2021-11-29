from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(channel=72) # A FEW PARAMETERS CAN BE SET BY THE PROGRAMMER
micropython.kbd_intr(-1)
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

while True:

	# INITIALISE COMMAND OUTPUT STRING
    command = ""

	# ARM THE DRONE USING BOTH BUTTONS
	# INCREASE THROTTLE WITH B BUTTON
	# CHECK OUT is_pressed() AND was_pressed() FUNCTIONS 
	# FIGURE OUT WHICH FUNCTION IS BETTER SUITED FOR THE CONTROLLER
            
    if button_a.is_pressed():
        if button_b.is_pressed():
            display.scroll(arm)
            if arm == 0:
                arm = 1
            else:
                arm = 0
        else:
            display.scroll("A")
            throttle -= 5
        
    if button_b.is_pressed():
        if button_a.is_pressed():
            display.scroll(arm)
            if arm == 0:
                arm = 1
                
            else:
                arm = 0
        else:
            display.scroll("B")
            throttle += 5

	# USE ACCLEREROMETER CLASS FOR DEALING WITH ROLL, PITCH AND YAW (X, Y AND Z AXES)
	# FIND APPROPRIATE VALUES FOR EACH TO SEND ACROSS TO DRONE
	
    curr_r = accelerometer.get_x() # roll
    if prev_r > curr_r and roll > -45:
        roll -= 3
        #print(roll)
    elif curr_r > prev_r and roll < 45:
        roll +=3
        #print(roll)
    prev_r = curr_r
    
    curr_p = accelerometer.get_y() # pitch
    if prev_p > curr_p and pitch > -45:
        pitch -= 3
        #print(pitch)
    elif curr_p > prev_p and pitch < 45:
        pitch +=3
        #print(pitch)
    prev_p = curr_p
    
    #y = accelerometer.get_y() # pitch
    #z = accelerometer.get_z() # yaw
    #print(x)
    #print(y)
    #print(z)
    
    # shake command
    #if accelerometer.is_gesture("shake"):
        #arm = 0
        
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    radio.send("P_" + str(pitch))
    radio.send("A_" + str(arm))
    radio.send("R_" + str(roll))
    radio.send("T_" + str(throttle))
    #radio.send("Y" + str(yaw))
    
    sleep(100) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE

