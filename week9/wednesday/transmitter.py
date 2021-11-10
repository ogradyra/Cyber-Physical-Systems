from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

# INITIALISE COMMANDS
x = 0 # roll
y = 0 # pitch
z = 0 # throttle (height)
arm = 0

display.off()
height = 0
s = 0

# time
d = utime.ticks_ms()

def rotary_encoder():
    global height, s 
    
    # orange = A
    a = pin3.read_analog()
    # green = B
    b = pin0.read_analog()
    
    if a > 512:
        a = 1
    else:
        a = 0
        
    if b > 512:
        b = 1
    else:
        b = 0
    
    #print("A: ", a, " B: ", b)
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
  
    if b != a and s == 0:
        # throttle increasing
        height = height + int(a)
        # throttle decreasing 
        height = height - int(b)
        #flag high
        s = 1
        
    elif b == 0 and a == 0:
        s = 0
    
    #print("Height: ", height)
    
def toggle():
    global x, y
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()
   
    #print("Pitch: ", pitch, "| Roll: ", roll)
    
    # convert to x and y coordinates
    if pitch < 100:
        y = 10
    elif pitch > 100 and pitch < 200:
        y = 8
    elif pitch > 200 and pitch < 300:
        y = 6
    elif pitch > 300 and pitch < 400:
        y = 4
    elif pitch > 400 and pitch < 500:
        y = 2
    elif pitch > 500 and pitch < 600:
        y = 0
    elif pitch > 600 and pitch < 700:
        y = -2
    elif pitch > 700 and pitch < 800:
        y = -4
    elif pitch > 800 and pitch < 900:
        y = -6
    elif pitch > 900 and pitch < 1000:
        y = -8
    else:
        y = -10
        
    if roll < 100:
        x = -10
    elif roll > 100 and roll <200:
        x = -8
    elif roll > 200 and roll < 300:
        x = -6
    elif roll > 300 and roll < 400:
        x = -4
    elif roll > 400 and roll < 500:
        x = -2
    elif roll > 500 and roll < 600:
        x = 0
    elif roll > 600 and roll < 700:
        x = 2
    elif roll > 700 and roll < 800:
        x = 4
    elif roll > 800 and roll < 900:
        x = 6
    elif roll > 900 and roll < 1000:
        x = 8
    else:
        x = 10
    
    print("X: ", x, " Y: ", y)

while True:
    
    # retrieve height (z coordinate)
    rotary_encoder()
    # retrieve x and y coordinates from pitch and roll
    toggle()

	# ON
    if button_a.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            throttle = 0
            arm = 1
        else:
            arm = 0
    
    # OFF
    if button_b.is_pressed():
        arm = 0
        throttle_s = 0
    
    
    if utime.ticks_add(utime.ticks_ms(), -d) >= 50 or utime.ticks_add(utime.ticks_ms(), -d) < 0:
        radio.send(str(x) + "," + str(y) + "," + str(z) + "," + str(arm))
        d = utime.ticks_ms()
    
    #print(d)
    
    # sleep(50)
