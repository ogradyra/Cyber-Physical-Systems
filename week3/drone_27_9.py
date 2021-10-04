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
a_int = 0
roll = 0
throttle = 0
yaw = 0
flight_mode = 45*5 + 512
buzzer = 0

pitch_id = 1
arm_id = 4
roll_id = 0
throttle_id = 2
yaw_id = 3
fm_id = 5
buzzer_id = 6
 
buf = bytearray(16)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receive_data():
    global pitch, roll, throttle, arm
    
    split_string = incoming.split("_")
    display.show(Image.HEART)
        
    if (split_string[0] == 'P'):
        pitch = split_string[1]
            
    elif (split_string[0] == 'A'):
        arm = split_string[1]
        #print(arm)
        
    elif (split_string[0] == 'R'):
        roll = split_string[1]
            
    elif (split_string[0] == 'T'):
        throttle = split_string[1]
            
    else:
        print('error')
        
def scaleTheNumbers(string_letter):
    # To-do: Flight mode is going to be 45. Add this into the logic
    if(string_letter == pitch):
        p = int(pitch) * 3.5 + 512
        return int(p)
    elif(string_letter == arm):
        a = 180*5
        return a
    elif(string_letter == roll):
        r = int(roll) * 3.5 + 521
        return int(r)
    elif(string_letter == throttle):
        t = int(throttle) * 512 / 50
        return int(t)
    #elif(string_letter == 'Y'):
       # To-Do: Add Yaw logic

while True:
    
    sleep(100)
    
    incoming = radio.receive()
    
    if (incoming != None):
        # retrieve values for p,a,r,t
        receive_data()
    
    # Scale and offset values
    p_int = scaleTheNumbers(pitch)
    if (arm == '1'):
        a_int = scaleTheNumbers(arm)
    else:
        a_int = 0
        #print("in:", a_int)
    r_int = scaleTheNumbers(roll)
    t_int = scaleTheNumbers(throttle)
    
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
        buf[5] = pitch 
        
    if ( t_int > 255):
        buf[6] =  t_int >> 8 
        buf[7] =  t_int 
    else:
        buf[6] = throttle_id << 2 
        buf[7] = t_int 
    
    if (yaw > 255):
        buf[8] = yaw >> 8 
        buf[9] = yaw 
    else:
        buf[8] = yaw_id << 2 
        buf[9] = yaw 
    
    if (a_int > 255):
        buf[10] = a_int >> 8 
        buf[11] = a_int 
    else:
        buf[10] = arm_id << 2 
        buf[11] = a_int 
        
    buf[12] = flight_mode >> 8 
    buf[13] = flight_mode 
    buf[14] = buzzer_id << 2 
    buf[15] = buzzer 
    
    print(buf)
    uart.write(buf)
        
