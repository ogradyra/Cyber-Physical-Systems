from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

# INITIALISE COMMANDS
pitch = 0
pitch_s = 0
arm = 0
roll = 0
throttle = 0
throttle_s = 0
roll_s = 0
yaw = 0

prev_r = 0
prev_p = 0
prev_y = 0

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1

total_battery: float = 0


incoming = 0
battery = 0
tele_roll = 0

# use LEDs on controller to track throttle, arm, pitch and roll values
def ledDisplay():
    # Arm
    if arm == 1:
        display.set_pixel(0, 0, 9)
    else:
        display.set_pixel(0, 0, 0)

    # Throttle
    # Pixel position moves as the throttle number increases
    global pixel_y
    old_pixel_y = pixel_y
    display.set_pixel(0, old_pixel_y, 0)  # To clear old pixel

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
    display.set_pixel(old_pr_pixel_x, old_pr_pixel_y, 0)  # To clear old pixel

    values = [-20, -10, 0, 10, 20]  # List of values
    # Roll is -20 on LHS and 20 on RHS
    # Pitch is 20 going forward and -20 going backwards
    for x in values:
        if roll_s == x:
            # Set the pixel roll value to the index of the match value
            pr_pixel_x = values.index(x)
            break

    for y in values:
        if pitch_s == y:
            # At 20, pixel should be 0, and at -20, pixel should be 4
            # Opposit way round to roll
            pr_pixel_y = (values.index(y) - 4) * (-1)
            break

    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)
    
def receive_data():
    global incoming, battery, tele_roll
    incoming = str(radio.receive())
    split_string = incoming.split("_")

    for i in range(len(split_string)):
        if split_string[i] == "Battery":
            battery = int(split_string[i + 1])
            #print(battery)

        elif split_string[i] == "Roll":
            tele_roll = int(split_string[i + 1])
            
    #print("Roll: " + tele_roll)

    
def fixRoll():
    global tele_roll
    #tele_roll = float(tele_roll)
    error = roll_s - tele_roll
    print("Error: ", error, "Roll: ", roll_s, "Tele Roll: ", tele_roll)
    
while True:
    receive_data()
    fixRoll()

    # check for low battery
    #battery = radio.receive()

    if battery:
        b = float(battery)
        if b < 0.2:
            display.show(Image.SKULL)
        total_battery = total_battery + b

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
        
    if roll >= 0 and roll < 100:
        roll_s = -20
    elif roll >= 100 and roll < 200:
        roll_s = -15
    elif roll > 200 and roll < 300:
        roll_s = -10
    elif roll > 300 and roll < 400:
        roll_s = -5
    elif roll > 400 and roll < 500:
        roll_s = 0
    elif roll > 500 and roll < 600:
        roll_s = 5
    elif roll > 600 and roll < 700:
        roll_s = 10
    elif roll > 700 and roll < 800:
        roll_s = 15
    elif roll > 800 and roll <= 1023:
        roll_s = 20
    else:
        roll_s = 0
        print("Error with roll")
        
    if pitch >= 0 and pitch < 200:
        pitch_s = -20
    elif pitch > 200 and pitch < 400:
        pitch_s = -10
    elif pitch > 400 and pitch < 600:
        pitch_s = 0
    elif pitch > 600 and pitch < 800:
        pitch_s = 10
    elif pitch > 800 and pitch <= 1023:
        pitch_s = 20
    else:
        pitch_s = 0
        print("Error with roll")
  
    #print("Roll", roll, "Scaled Roll:",roll_s, "Pitch:", pitch)
    
    # shake command
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle_s = 0
    
    ledDisplay()
	# UPDATE COMMAND STRING TO BE SENT OUT WITH CONCATENATED PARTY COMMANDS
    radio.send("P_" + str(pitch_s) + "_A_" + str(arm) + "_R_" + str(roll_s) + "_T_" + str(throttle_s) + "_Y_" + str(0))
    #radio.send(str(0) + "," + str(arm) + "," + str(0) + "," + str(throttle_s) + "," + str(0))
    
    
    sleep(50) # sleep() IS YOUR FRIEND, FIND GOOD VALUE FOR LENGTH OF SLEEP NEEDED TO FUNCTION WITHOUT COMMANDS GETTING MISSED BY THE DRONE
