# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import utime

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)
radio.on()  # Radio won't work unless it's on
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)
micropython.kbd_intr(-1)
incoming = 0
buzzer = 0

# Scaled variables

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


uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1

scaling = 3.5
offset = 512

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receive_data():
    global pitch, roll, throttle, arm, yaw

    split_string = incoming.split("_")

    for i in range(len(split_string)):
        if split_string[i] == "P":
            pitch = split_string[i + 1]

        elif split_string[i] == "A":
            arm = split_string[i + 1]

        elif split_string[i] == "R":
            roll = split_string[i + 1]

        elif split_string[i] == "T":
            throttle = split_string[i + 1]

        elif split_string[i] == "Y":
            yaw = split_string[i + 1]
        # print(split_string[i])

def ledDisplay():
    # Arm
    
    if arm == "1":
        display.set_pixel(0, 0, 9)
    else:
        display.set_pixel(0, 0, 0)

    # Throttle
    # Pixel position moves as the throttle number increases
    global pixel_y
    old_pixel_y = pixel_y
    display.set_pixel(0, old_pixel_y, 0)  # To clear old pixel

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
    display.set_pixel(old_pr_pixel_x, old_pr_pixel_y, 0)  # To clear old pixel
    
    r = int(roll)
    p = int(pitch)
    
    values = [-20, -10, 0, 10, 20] # List of roll values
    # Roll is -20 on LHS and 20 on RHS
    # Pitch is 20 going forward and -20 going backwards
    for x in values:
        if r == x:
            # Set the pixel roll value to the index of the match value
            pr_pixel_x = values.index(x) 
            break
        
    for y in values:
        print(y);
        if p == y:
            # At 20, pixel should be 0, and at -20, pixel should be 4
            # Opposit way round to roll
            pr_pixel_y = (values.index(y) - 4) * (-1) 
            break
  
    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)

# displays % charging on LEDs 
# warns controller if battery charge on drone is less than 20 %
def battery_read():
    battery = pin0.read_analog()
    radio.send(str(battery))
    
    charge = ((battery-300)/(1023-300))
    #print(charge)
    if charge >= 0.6 and charge < 0.8:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 9)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge >= 0.4 and charge < 0.6:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 0)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge >= 0.2 and charge < 0.4:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 0)
        display.set_pixel(4, 2, 0)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge < 0.2:
        display.show(Image.SKULL)

    else:
        display.set_pixel(4, 0, 9)
        display.set_pixel(4, 1, 9)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

def read_into():
    
    buf_size = 16
    buf = bytearray(buf_size)
    
    global t_int, y_int
    flight_mode = 45 * 5

    p_int = int(pitch) * 3.5 + 512
    p_int = int(p_int)

    if arm == "1":
        a_int = 180 * 5
    else:
        a_int = 0

    r_int = int(roll) * 3.5 + 521
    r_int = int(r_int)

    t_int = int(throttle) * 512 / 50
    t_int = int(t_int)

    y_int = int(yaw) * 5 + 512
    y_int = int(y_int)
    
    buf = bytearray(16)
    buf[0] = 0
    buf[1] = 0x01
    buf[2] = (0 << 2) | ((r_int >> 8) & 3)
    buf[3] = r_int & 255
    buf[4] = (1 << 2) | ((p_int >> 8) & 3)
    buf[5] = p_int & 255
    buf[6] = (2 << 2) | ((t_int >> 8) & 3)
    buf[7] = t_int & 255
    buf[8] = (3 << 2) | ((y_int >> 8) & 3)
    buf[9] = y_int & 255
    buf[10] = (4 << 2) | ((a_int >> 8) & 3)
    buf[11] = a_int & 255
    buf[12] = (5 << 2) | ((flight_mode >> 8) & 3)
    buf[13] = flight_mode & 255
    buf[14] = (6 << 2) | ((0 >> 8) & 3)
    buf[15] = 0 & 255
    
    uart.write(buf)
    print(buf)
    # https://stackoverflow.com/questions/59908012/what-are-t-and-r-in-byte-representation
    
while True:
    

    incoming = radio.receive()
    
    if incoming:
        receive_data()
        read_into()
        ledDisplay()
        battery_read()
        sleep(50)
    else:
        print("No Incoming Data")

    
