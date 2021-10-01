# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython

radio.on() # Radio won't work unless it's on
radio.config(channel=72)
micropython.kbd_intr(-1)
incoming = 0

pitch = 0
arm = 0
roll = 0
throttle = 0
yaw = 0
flight_mode = 0
buzzer = 0

# Scaled variables
p_int = 0
a_int = 0
r_int = 0
t_int = 0
y_int = 0

roll_id = 0
pitch_id = 1
throttle_id = 2
yaw_id = 3
arm_id = 4
flight_mode_id = 5
buzzer_id = 6
 
buf = bytearray(16)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receive_data():
    global pitch, roll, throttle, arm
    
    split_string = incoming.split("_")
    
    for i in range(len(split_string)):
        if (split_string[i] == 'P'):
            pitch = split_string[i+1]
            
        elif (split_string[i] == 'A'):
            arm = split_string[i+1]
            
        elif (split_string[i] == 'R'):
            roll = split_string[i+1]
            
        elif (split_string[i] == 'T'):
            throttle = split_string[i+1]
        
        elif (split_string[i] == 'Y'):
            yaw = split_string[i+1]
        print(split_string[i])

def scaleNum():
    global flight_mode, p_int, a_int, r_int, t_int, y_int
    flight_mode = 45*5 + 512
    
    p_int = int(pitch) * 3.5 + 512
    p_int = int(p_int)

    if(arm == '1'):
        a_int = 180*5
    else:
        a_int = 0
    
    r_int = int(roll) * 3.5 + 521
    r_int = int(r_int)

    t_int = int(throttle) * 512 / 50
    t_int = int(t_int)
    
    y_int = int(yaw) * 5 + 512
    y_int = int(y_int)
    print("PART:", p_int, a_int, r_int, t_int, y_int)
    #elif(string_letter == 'Y'):
       # To-Do: Add Yaw logic
       

def ledDisplay():
    # Arm
    if a_int > 0:
        display.set_pixel(0,0,9)
    else:
        display.set_pixel(0,0,0)
    
    # Throttle
    # Pixel position moves as the throttle number increases
    global pixel_y
    old_pixel_y = pixel_y
    display.set_pixel(0, old_pixel_y, 0) # To clear old pixel
    
    if t_int < 256:
        pixel_y = 4
    elif t_int < 512:
        pixel_y = 3
    elif t_int < 768:
        pixel_y = 2
    else:
        pixel_y = 1
        
    display.set_pixel(0, pixel_y, 9)
    
    # Pitch and Roll
    global pr_pixel_x, pr_pixel_y
    old_pr_pixel_x = pr_pixel_x
    old_pr_pixel_y = pr_pixel_y
    display.set_pixel(old_pr_pixel_x, old_pr_pixel_y, 0) # To clear old pixel
    

    if (r_int < 426):
        pr_pixel_x = 0
    elif (r_int < 489):
        pr_pixel_x = 1
    elif (r_int < 552):
        pr_pixel_x = 2
    elif (r_int < 615):
        pr_pixel_x = 3
    else:
        pr_pixel_x = 4
    
    
    if (p_int < 417):
        pr_pixel_y = 0
    elif (p_int < 480):
        pr_pixel_y = 1
    elif (p_int < 543):
        pr_pixel_y = 2
    elif (p_int < 606):
        pr_pixel_y = 3
    else:
        pr_pixel_y = 4
    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)


while True:
    sleep(100)
    
    incoming = radio.receive()
    if (incoming != None):
        receive_data()
    else:
        print("No Incoming Data")
    
    # Scale and offset values
    scaleNum()
    
    
    # parse into buffer
    buf[0] = 0
    buf[1] = 0x01
    
    if (r_int > 255):
        buf[2] = r_int >> 8
        buf[3] = r_int
    else:
        buf[2] = roll_id << 2 
        buf[3] = r_int 
    
    if (p_int > 255):
        buf[4] = p_int >> 8 
        buf[5] = p_int 
    else:
        buf[4] = pitch_id << 2 
        buf[5] = p_int 
        
    if (t_int > 255):
        buf[6] =  t_int >> 8 
        buf[7] =  t_int 
    else:
        buf[6] = throttle_id << 2 
        buf[7] = t_int 
    
    if (y_int > 255):
        buf[8] = y_int >> 8 
        buf[9] = y_int 
    else:
        buf[8] = yaw_id << 2 
        buf[9] = y_int 
    
    if (a_int > 255):
        buf[10] = (a_int >> 8) & 255 
        buf[11] = (a_int) & 255 
    else:
        buf[10] = (arm_id << 2) & 255 
        buf[11] = (a_int) & 255 
    
    if (flight_mode > 255):
        buf[12] = flight_mode >> 8 
        buf[13] = flight_mode
    else:
        buf[12] = flight_mode_id << 2 
        buf[13] = flight_mode    
     
    buf[14] = buzzer_id << 2 
    buf[15] = buzzer 
    
    print(buf)
    print(buf[2])
    uart.write(buf)
    
    ledDisplay()
        
