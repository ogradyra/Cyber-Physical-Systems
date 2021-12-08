from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime
import music

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

# INITIALISE COMMANDS
x = 0 # roll
y = 0 # pitch
arm = 0
throttle = 0

display.off()
height = 0
s = 0
height_wanted = 40  #24 pulse in one rotation, we want 4 rotations. 96 pulses
height_error = 0

# time
d = utime.ticks_ms()

throttle_flag = 0

def battery_display(battery):
    
    charge = ((battery-300)/(1023-300))
    #print(charge)
    
    # communication from drone to controller
    # Can't access the display because of analogs pins that are in use, so use music tone instead to indicate when battery low
    if charge < 0.2:
        music.play(music.DADADADUM)  
        # arm = 0?

# function to retrieve height 
def rotary_encoder():
    global height, s 
    
    # orange = A
    a_in = pin4.read_analog()
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
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
    
    # if signals not equal, pulse has occured, either up or down
    if b != a and s == 0:
        # throttle increasing
        height = height + int(a)
        # throttle decreasing 
        height = height - 2*(int(b))
        #flag high
        s = 1
    
    # condition so that same pulse isn't counted twice - both signals must go to 0 again before another pulse can be counted
    elif b == 0 and a == 0:
        s = 0
    
    #print("Height: ", height)
    
# function to retrieve the pitch and roll values
def toggle():
    global x, y
    
    roll = pin1.read_analog()
    pitch = pin2.read_analog()
   
    # convert to x and y coordinates
    # only vary the pitch and roll between -10 and 10 so drone doesn't lean too much
    
    if pitch > 812:
        y = 0
    elif pitch < 212:
        y = 0
    else:
        y = 0
        
    
    if roll > 812:
        x = 0
    elif roll < 212:
        x = 0
    else:
        x = 0
    
    '''y = pitch - 512
    if y != 0:
        y = y/abs(y)
        
    x = roll - 512
    if x != 0:
        x = x/abs(x)'''
    
    #print("X: ", x, " Y: ", y)
    print("Pitch: ", pitch, " Roll: ", roll)

while True:
    
    message = radio.receive()
    if message:
        contents = message.split(',')
        #print("Message: ", contents)
        if contents[0] == '1':
            if contents[1] == '0':
                print("Battery: ", contents[2])
                battery_display(int(contents[2]))
    
    # retrieve height
    rotary_encoder()
    # retrieve x and y coordinates from pitch and roll
    toggle()

	# ON
    if button_a.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
            throttle_flag = 0
            height = 0
        else:
            arm = 0
            
    # Switch to height based throttle
    if button_b.is_pressed():
        throttle_flag = 1
    
    # if the difference in ticks between d (value saved when the program is first run) and ticks that have elapsed since is greater than 50, send radio data
    # might have to change ticks_add to ticks_diff ??
    # this statement acts as the sleep
    if utime.ticks_diff(utime.ticks_ms(), d) >= 100 or utime.ticks_diff(utime.ticks_ms(), d) < 0:
        radio.send("0" + "," + "0" + "," + str(int(x)) + "," + str(int(y)) + "," + str(height) + "," + str(arm) + "," + str(throttle_flag))
	    # reset d, so this code can execute every 50 ms
        d = utime.ticks_ms()
