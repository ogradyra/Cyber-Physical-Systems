from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import time

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

# INITIALISE COMMANDS
pitch = 0
arm = 0
roll = 0
throttle = 0
yaw = 0

display.off()

p_up = 0
p_down = 0
r_up = 0
r_down = 0

# BEGIN PID TERMS
p = 0
i = 0
d = 0

prev_output = 0
prev_e = 0
prev_y = 0

target_p = 512
target_r = 521
target_h = 100

# coefficients
kp = 0.5
ki = 0.1
kd = 0
    
# timing
sample_time = 0.02
curr_time = time()
old_time = curr_time
# END PID TERMS

def receive_data():
    global r_up
    
    # orange = A
    a = pin3.read_digital()
    # green = B
    b = pin0.read_digital()
    
    #print("A: ", a, " B: ", b)
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
   
    #print(a, a_prev_state)
    
    if a != a_prev_state:
        if b != a:
            # throttle increasing
            p_up = p_up + 1
            
        elif b == a:
            # throttle decreasing       
            p_down = p_down + 1
                
        #print(position)    
        
    a_prev_state = a
    print("P up: ", p_up, "|", "P down: ", p_down)
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()


def PID(y, target):
    
    # error between target and recieved value from toggle / rotary encoder
    e = target - y
    
    # calculate change in time
    curr_time = time()
    dt = curr_time - old_time
    
    # update values every sampling period
    if dt >= sample_time:
        # proportional
        p = kp*e
        # integral
        i = ki*e*dt
        # derivative
        d = kd*(prev_y-y)/dt
        
        # update values
        prev_e = e
        old_time = curr_time
        prev_y = y
        
        # updated roll or pitch value
        output = p + i + d
        
    return int(output)

def throttle_convert():
    # convert a height to the correct throttle?
    # start with a high throttle, as height error decreases, reduce throttle
    # convert from height to throttle then do a PID for throttle??
    
while True:
    
    receive_data()

	# ARM COMMAND
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
        else:
            arm = 0
    
    # SHAKE COMMAND
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle_s = 0
        
    # CONTROLLER
    pitch = PID(pitch, target_p)
    roll = PID(roll, target_r)
    throttle = PID(r_up, target_h)
    
    radio.send("P_" + str(pitch) + "_A_" + str(arm) + "_R_" + str(roll) + "_T_" + str(throttle) + "_Y_" + str(yaw))
    
    sleep(50) 
