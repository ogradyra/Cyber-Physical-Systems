from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=2) 

# INITIALISE COMMANDS
# REMEMBER PARTY
pitch = 0
arm = 0
roll = 0
throttle = 0
throttle_s = 0
yaw = 0

# NO NEED TO MAKE FUNCTIONS FOR THIS CONTROLLER
# JUST USE WHILE LOOP

prev_r = 0
prev_p = 0
prev_y = 0

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1

total_battery: float = 0

# use LEDs on controller to track throttle, arm, pitch and roll values
def ledDisplay():
    # Arm
    if arm == 1:
        display.set_pixel(0,0,9)
    else:
        display.set_pixel(0,0,0)
    
    # Throttle
    # Pixel position moves as the throttle number increases
    global pixel_y
    old_pixel_y = pixel_y
    display.set_pixel(0, old_pixel_y, 0) # To clear old pixel
    
    if throttle_s < 25:
        pixel_y = 4
    elif throttle_s < 50:
        pixel_y = 3
    elif throttle_s < 75:
        pixel_y = 2
    else:
        pixel_y = 1
        
    display.set_pixel(0, pixel_y, 9)
    
    # Pitch and Roll
    global pr_pixel_x, pr_pixel_y
    old_pr_pixel_x = pr_pixel_x
    old_pr_pixel_y = pr_pixel_y
    display.set_pixel(old_pr_pixel_x, old_pr_pixel_y, 0) # To clear old pixel
    
    if (roll < -27):
        pr_pixel_x = 0
    elif (roll < -9):
        pr_pixel_x = 1
    elif (roll < 9):
        pr_pixel_x = 2
    elif (roll < 27):
        pr_pixel_x = 3
    else:
        pr_pixel_x = 4
    
    if (pitch < -27):
        pr_pixel_y = 0
    elif (pitch < -9):
        pr_pixel_y = 1
    elif (pitch < 9):
        pr_pixel_y = 2
    elif (pitch < 27):
        pr_pixel_y = 3
    else:
        pr_pixel_y = 4
    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)
    
    
while True:

    # check for low battery
    battery = radio.receive()
    
    if battery:
        b = float(battery)
        
        if b < 0.2:
            display.show(Image.SKULL)
            
        total_battery = total_battery + b

        #print("Battery level:", (b / 1023) * 3.3, "V")
            
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
    
    # if button_a.was_pressed() and throttle >= 5: # Min value of throttle is 0
    #     throttle -= 5
        
    # if button_b.was_pressed() and throttle <= 95: # Max value of throttle is 100
    #     throttle += 5
    
	# USE ACCLEREROMETER CLASS FOR DEALING WITH ROLL, PITCH AND YAW (X, Y AND Z AXES)
	# FIND APPROPRIATE VALUES FOR EACH TO SEND ACROSS TO DRONE
	
    curr_r = accelerometer.get_x() # roll
    if prev_r > curr_r and roll > -45:
        roll -= 3
    elif curr_r > prev_r and roll < 45:
        roll +=3
    prev_r = curr_r
    
    # pitch -> Drone tilts forward and moves forward.
    # Back two engines turn on
    curr_p = accelerometer.get_y() 
    if prev_p > curr_p and pitch > -45:
        pitch -= 3
    elif curr_p > prev_p and pitch < 45:
        pitch +=3
    prev_p = curr_p
    
    # yaw -> Changes where the front of the drone is facing (but dont move forwards
    # or backwards) Like twisting the lid of a bottle. Lid doesn't leave its position
    # but it does move
    curr_y = accelerometer.get_z() 
    #print(curr_y)
    if prev_y > curr_y and yaw > -30:
        yaw -= 3
    elif curr_y > prev_y and yaw < 30:
        yaw += 3
    prev_y = curr_y
    
    #z = accelerometer.get_z() # yaw
    #print(x)
    #print(y)
    #print(z)
    
    throttle = pin0.read_analog()
    # throttle_scaled = throttle/10
    if throttle < 100:
        throttle_s = 0
    elif throttle > 100 and throttle <200:
        throttle_s = 10
    elif throttle > 200 and throttle <300:
        throttle_s = 20
    elif throttle > 300 and throttle <400:
        throttle_s = 30
    elif throttle > 400 and throttle <500:
        throttle_s = 40
    elif throttle > 500 and throttle <600:
        throttle_s = 50
    elif throttle > 600 and throttle <700:
        throttle_s = 60
    elif throttle > 700 and throttle <800:
        throttle_s = 70
    elif throttle > 800 and throttle <900:
        throttle_s = 80
    elif throttle > 900 and throttle <1000:
        throttle_s = 90
    else:
        throttle_s = 100
        
    #roll = pin1.read_analog()
    #pitch = pin2.read_analog()
    print("Throttle:",throttle, "Scaled Throttle",throttle_s, "Roll:",roll, "Pitch:", pitch)
    
    # shake command
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle_s = 0
    
    ledDisplay()
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    #radio.send("P_" + str(0) + "_A_" + str(arm) + "_R_" + str(0) + "_T_" + str(throttle_s))
    radio.send(str(0) + "," + str(arm) + "," + str(0) + "," + str(throttle_s) + "," + str(0))

    #radio.send("Y" + str(yaw))
    #print(throttle)
    
    sleep(50) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE
