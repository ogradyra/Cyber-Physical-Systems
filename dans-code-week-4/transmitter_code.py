from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(channel=6) # A FEW PARAMETERS CAN BE SET BY THE PROGRAMMER

# INITIALISE COMMANDS
# REMEMBER PARTY
Pitch = 0
Arm = 0
Roll = 0
Throttle = 0
Yaw = 0
start = 0
# NO NEED TO MAKE FUNCTIONS FOR THIS CONTROLLER
# JUST USE WHILE LOOP

while True:
	# INITIALISE COMMAND OUTPUT STRING
    if button_a.is_pressed() and button_b.is_pressed():
        #if utime.ticks_diff(utime.ticks_ms(), start) > 500:
        #start = utime.ticks_ms()
        if Arm == 1:
            Arm = 0
            Throttle = 0
            display.set_pixel(2, 2, 0)
            sleep(50)
        else:
            Arm = 1
            display.set_pixel(2, 2, 9)
            sleep(50)

#Failsafe
    if accelerometer.was_gesture("shake"):
        Arm = 0
        display.set_pixel(2, 2, 0)

#Controlling the throttle
    if button_b.was_pressed():
        if Throttle < 100:
            Throttle = Throttle + 5
        else:
            Throttle = 100
    if button_a.was_pressed():
        if Throttle > 0:
            Throttle = Throttle - 5
        else:
            Throttle = 0

#Controlling pitch and roll
    axis_y = accelerometer.get_y()
    axis_x = accelerometer.get_x()

    if axis_x > 300:
        Roll = 20
    elif axis_x < -300:
        Roll = -20
    else:
        Roll = 0

    if axis_y < -300:
        Pitch = 20
    elif axis_y > 300:
        Pitch = -20
    else:
        Pitch = 0

    command =  str(Pitch) + ", " + str(Arm) + ", " + str(Roll) + ", " + str(Throttle) + ", " + str(Yaw)

    radio.send(command)
    sleep(50)
    """
    if button_a.was_pressed() and button_b.was_pressed():
        Arm = 1
        Throttle = 0

    if button_a.is_pressed():
        Throttle -= 5

    if button_b.is_pressed():
        Throttle += 5

    Pitch = int(-accelerometer.get_y()/6)
    Roll = int(accelerometer.get_x()/6)
    print("Pitch: ", Pitch)
    print("Roll: ", Roll)

    #Yaw?

    if accelerometer.was_gesture("shake"):
        Arm = 0
        Throttle = 0




	# ARM THE DRONE USING BOTH BUTTONS

	# INCREASE THROTTLE WITH B BUTTON

	# CHECK OUT is_pressed() AND was_pressed() FUNCTIONS

	# FIGURE OUT WHICH FUNCTION IS BETTER SUITED FOR THE CONTROLLER



	# USE ACCLEREROMETER CLASS FOR DEALING WITH ROLL, PITCH AND YAW (X, Y AND Z AXES)

	# FIND APPROPRIATE VALUES FOR EACH TO SEND ACROSS TO DRONE



	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS



    sleep(50) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE
    """
