from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

display.off()

pitch_target = 0 # roll
roll_target  = 0 # pitch

arm    = 0
height = 0
s      = 0

# Time to transmit data
d = utime.ticks_ms()

throttle_flag = 0

# function to retrieve height 
def rotary_encoder():
    global height, s 
    
    # orange = A
    a_in = pin3.read_analog()
    # green = B
    b_in = pin0.read_analog()
    
    # if signal is ON, set a or b to 1, if signal is OFF, set a or b to 0
    if a_in > 512:
        a = 1
    else:
        a = 0
        
    if b_in > 512:
        b = 1
    else:
        b = 0
    
    #print("A: ", a, " B: ", b)
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
    
    # if signals not equal, pulse has occured, either up or down
    if b != a and s == 0:
        # throttle increasing
        height = height + int(a)
        # throttle decreasing 
        height = height - int(b)
        #flag high
        s = 1
    
    # condition so that same pulse isn't counted twice - both signals must go to 0 again before another pulse can be counted
    elif b == 0 and a == 0:
        s = 0
    
    
# function to retrieve the pitch and roll target values
def toggle():
    global pitch_target, roll_target
    
    x_position = pin1.read_analog()
    y_position = pin2.read_analog()
   
    # convert to x and y coordinates
    # only vary the pitch and roll between -10 and 10 so drone doesn't lean too much
    
    if y_position > 812:
        pitch_target = 10
    elif y_position < 212:
        pitch_target = -10
    else:
        pitch_target = 0
    
    if x_position > 812:
        roll_target = 10
    elif x_position < 212:
        roll_target = -10
    else:
        roll_target = 0

while True:
    
    # retrieve height
    rotary_encoder()
    # retrieve x and y coordinates from pitch and roll
    toggle()

	# Arm
    if button_a.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
            throttle_flag = 0
            height = 0
        else:
            arm = 0
    
    # Activate
    if button_b.is_pressed():
        throttle_flag = 1
    
    # if the difference in ticks between d (value saved when the program is first run) and ticks that have elapsed since is greater than 50, send radio data
    # might have to change ticks_add to ticks_diff ??
    if utime.ticks_diff(utime.ticks_ms(), -d) >= 50 or utime.ticks_diff(utime.ticks_ms(), -d) < 0:
        radio.send(str(pitch_target) + "," + str(roll_target) + "," + str(height) + "," + str(arm) + "," + str(throttle_flag))
	    # reset d, so this code can execute every 50 ms
        d = utime.ticks_ms()
