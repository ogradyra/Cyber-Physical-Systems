from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config() # A FEW PARAMETERS CAN BE SET BY THE PROGRAMMER

# INITIALISE COMMANDS
# REMEMBER PARTY
Pitch = 0
Arm = 0
Roll = 0
Throttle = 0
Yaw = 0

# NO NEED TO MAKE FUNCTIONS FOR THIS CONTROLLER
# JUST USE WHILE LOOP


while True:

	# INITIALISE COMMAND OUTPUT STRING
    command = ""

	# ARM THE DRONE USING BOTH BUTTONS
	# INCREASE THROTTLE WITH B BUTTON
	# CHECK OUT is_pressed() AND was_pressed() FUNCTIONS 
	# FIGURE OUT WHICH FUNCTION IS BETTER SUITED FOR THE CONTROLLER

	# USE ACCLEREROMETER CLASS FOR DEALING WITH ROLL, PITCH AND YAW (X, Y AND Z AXES)
	# FIND APPROPRIATE VALUES FOR EACH TO SEND ACROSS TO DRONE

	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS

    sleep() # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE
