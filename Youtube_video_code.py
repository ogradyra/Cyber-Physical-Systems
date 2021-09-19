# https://www.youtube.com/watch?v=y5DkiL6gIzY&ab_channel=Makekit
# https://makecode.microbit.org/#editor

pitch = 0
arm = 0 #Arm means on or off for the drone
roll = 0
throttle = 0
yaw = 0
radio_group = 7
radio.set_group(radio_group)
# Have the display show the radio set_group
basic.show_number(radio_group)
# To show the radio group number on the display

# Function for when the a button is pressed on the transmitter
# Want to decrease the speed
# The input part is the inturrupt that detects the button being pressed
# The section above the input is the function part where we'll add our code
def on_button_pressed_a():
    global throttle
    throttle -= 5
input.on_button_pressed(Button.A, on_button_pressed_a)

# Function for when the b button is pressed on the transmitter
# Want to increase the speed
# Inside the functions, the varibales are local
# Need to specify that is the global variable we are changing
def on_button_pressed_b():
    global throttle
    throttle += 5
input.on_button_pressed(Button.B, on_button_pressed_b)

# To turn on and off the engines
def on_button_pressed_ab():
    global arm
    global throttle
    throttle = 0
    if arm == 0:
        arm = 1
    else:
        arm = 0
input.on_button_pressed(Button.AB, on_button_pressed_ab)

# Shake to stop feature
def on_gesture_shake():
    global arm
    arm = 0
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def on_forever():
    #basic.show_number(throttle) # To display value on the board
    pitch = input.rotation(Rotation.PITCH)
    roll = input.rotation(Rotation.ROLL)

    # To fill a pixel when the motors are turned on_button_pressed
    basic.clear_screen()
    if arm == 1:
        led.plot(0,0) # Top Left Pixel
    
    # Throttle
    led.plot(0, Math.map(throttle,0,100,4,0)) # How to represent throttle if only leds from 0 - 4
    # map(value you want to change, whats the lowest number it can be, whats the highest number it can be, 
    #       whats the lowest output number you want it to be, whats the highest output number you want it to be)

    # roll and pitch
    led.plot(Math.map(roll,-45, 45,0,4), Math.map(pitch,-45, 45,0,4)) # x-axis -> moves side to side, y-axis -> moves up and down
    
    # This function send 1 value with a name from transmitter to drone. Tells it whether it is roll or pitch or whatever and how much it is
    radio.send_value("P", pitch)
    radio.send_value("A", arm)
    radio.send_value("R", roll)
    radio.send_value("T", throttle)
    radio.send_value("Y", yaw)

basic.forever(on_forever)

