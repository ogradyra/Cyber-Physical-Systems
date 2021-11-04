from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47) 

# INITIALISE COMMANDS
pitch = 0
pitch_s = 0
arm = 0
roll = 0
throttle = 0
throttle_s = 0
roll_s=0
yaw = 0

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
    
    values = [-20, -10, 0, 10, 20] # List of roll values
    # Roll is -20 on LHS and 20 on RHS
    # Pitch is 20 going forward and -20 going backwards
    for x in values:
        if roll_s == x:
            # Set the pixel roll value to the index of the match value
            pr_pixel_x = values.index(x) 
            break
        
    for y in values:
        print(y);
        if pitch_s == y:
            # At 20, pixel should be 0, and at -20, pixel should be 4
            # Opposit way round to roll
            pr_pixel_y = (values.index(y) - 4) * (-1) 
            break
  
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
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
        else:
            arm = 0
    
    if button_a.was_pressed() and throttle >= 5: # Min value of throttle is 0
        throttle_s -= 5
        
    if button_b.was_pressed() and throttle <= 95: # Max value of throttle is 100
        throttle_s += 5
   
    roll = pin1.read_analog()
    pitch = pin2.read_analog()
    
    # ToDo: Uncomment below when throttle joystick wired up
    #throttle = pin0.read_analog()
    # throttle_scaled = throttle/10
    # throttle_s = int(throttle/10)
    # if throttle_s > 100:
    #     throttle_s = 100
        

    if roll/600 < 1: # Roll is num less than 600
        if roll/400 < 1: # Roll is num less than 400
            if roll/200 < 1: # Roll is num less than 200
                roll_s = -20
            else: # Roll is num less than 400 but greater than or equal to 200
                roll_s = -10
        else: # Roll is num less than 600 but greater than or equal to 400
            roll_s = 0
    elif roll/800 < 1: # Roll is num less than 800
        roll_s = 10
    else: # Roll is num greater than or equal to 800
        roll_s = 20
    
    if pitch/600 < 1: 
        if pitch/400 < 1: 
            if pitch/200 < 1: 
                pitch_s = -20
            else: 
                pitch_s = -10
        else: 
            pitch_s = 0
    elif pitch/800 < 1: 
        pitch_s = 10
    else: 
        pitch_s = 20
    
    print("Roll", roll, "Scaled Roll:",roll_s, "Pitch:", pitch, "Scaled Pitch:", pitch_s)
    
    # shake command
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle_s = 0
    
    ledDisplay()
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    radio.send("P_" + str(pitch_s) + "_A_" + str(arm) + "_R_" + str(roll_s) + "_T_" + str(throttle_s))
    #radio.send(str(0) + "," + str(arm) + "," + str(0) + "," + str(throttle_s) + "," + str(0))

    #radio.send("Y" + str(yaw))
    #print(throttle)
    
    sleep(50) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE