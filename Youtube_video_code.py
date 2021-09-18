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
    pass
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def on_forever():
    basic.show_number(throttle) # To display value on the board
basic.forever(on_forever)

