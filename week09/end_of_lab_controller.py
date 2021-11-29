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
height = 0

# BEGIN PID TERMS
p = 0
i = 0
d = 0

prev_output = 0
prev_e = 0
prev_y = 0

target_p = 512
target_r = 521
target_h = 10

# coefficients

# pitch
p_i = 0
p_e = 0
p_kp = 0
p_ki = 0
p_kd = 0

# roll
r_i = 0
r_e = 0
r_kp = 0
r_ki = 0
r_kd = 0

# throttle
t_i = 0
t_e = 0
t_kp = 0
t_ki = 0
t_kd = 0

s = 0

def receive_data():
    global height, s 
    
    # orange = A
    a = pin3.read_digital()
    # green = B
    b = pin0.read_digital()
    
    print("A: ", a, " B: ", b)
    
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
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()
    
    #print("Pitch: ", pitch, "| Roll: ", roll)

def PID(y, target, i, prev_e, kp, ki, kd):
    
    # error between target and recieved value from toggle / rotary encoder
    e = target - y
    
    # proportional
    p = kp*e
    # integral
    i += ki*e
    # derivative
    d = kd*(prev_e-e)
    
    # update values
    prev_e = e
    
    # updated roll or pitch value
    output = p + i + d
        
    return int(output)

    
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
    pitch = PID(pitch, target_p, p_i, p_e, p_kp, p_ki, p_kd)
    roll = PID(roll, target_r, r_i, r_e, r_kp, r_ki, r_kd)
    throttle = PID(height, target_h, t_i, t_e, t_kp, t_ki, t_kd)
    
    radio.send("P_" + str(pitch) + "_A_" + str(arm) + "_R_" + str(roll) + "_T_" + str(throttle) + "_Y_" + str(yaw))
    
    sleep(50)
