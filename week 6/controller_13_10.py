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
yaw = 0

pitch_s = 0
throttle_s = 0
roll_s=0

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
    
    if (roll_s == -20):
        pr_pixel_x = 0
    elif (roll_s == -10):
        pr_pixel_x = 1
    elif (roll_s == 0):
        pr_pixel_x = 2
    elif (roll_s == 10):
        pr_pixel_x = 3
    elif (roll_s == 20):
        pr_pixel_x = 4
    
    if (pitch_s == 20):
        pr_pixel_y = 0
    elif (pitch_s == 10):
        pr_pixel_y = 1
    elif (pitch_s == 0):
        pr_pixel_y = 2
    elif (pitch_s == -10):
        pr_pixel_y = 3
    elif (pitch_s == -20):
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
        

    # Arm        
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
        else:
            arm = 0
    
    # Throttle
    throttle = pin0.read_analog()
    roll = pin1.read_analog()
    pitch = pin2.read_analog()
    
   
    print("Roll", roll, "Scaled Roll:", roll_s, "Pitch:", pitch, "Scaled Pitch:", pitch)
    
    # shake command
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle_s = 0
    
    # INITIALISE COMMAND OUTPUT STRING
    command = ""
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    radio.send(str(pitch) + "," + str(arm) + "," + str(roll) + "," + str(throttle))
    
    ledDisplay()
    sleep(50) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE

