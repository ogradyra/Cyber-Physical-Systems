# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

radio.on()  # Radio won't work unless it's on
radio.config(length=251)
radio.config(channel=2)
radio.config(queue=1)
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

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1



def ledDisplay():
    # Arm
    if a_int > 0:
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
    
    if (r == -20):
        pr_pixel_x = 0
    elif (r == -10):
        pr_pixel_x = 1
    elif (r == 0):
        pr_pixel_x = 2
    elif (r == 10):
        pr_pixel_x = 3
    elif (r == 20):
        pr_pixel_x = 4
    
    p = int(pitch)
    
    if (p == 20):
        pr_pixel_y = 0
    elif (p == 10):
        pr_pixel_y = 1
    elif (p == 0):
        pr_pixel_y = 2
    elif (p == -10):
        pr_pixel_y = 3
    elif (p == -20):
        pr_pixel_y = 4
        
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


while True:
    
    incoming = radio.receive()
    
    if incoming:
        
        split_string = incoming.split(",")
    
        pitch = split_string[0]
        arm = split_string[1]
        roll = split_string[2]
        throttle = split_string[3]
        
        #print(throttle)
        
        p_int = int(pitch)
        r_int = int(roll)
        t_int = int(throttle)
        
        if arm == "1":
            a_int = 900
        else:
            a_int = 0
        
        buf = bytearray(16)
        buf[0] = 0
        buf[1] = 0x01
        buf[2] = (0 << 2) | ((r_int >> 8) & 3)
        buf[3] = r_int & 255
        buf[4] = (1 << 2) | ((p_int >> 8) & 3)
        buf[5] = p_int & 255
        buf[6] = (2 << 2) | ((t_int >> 8) & 3)
        buf[7] = t_int & 255
        buf[8] = (3 << 2) | ((512 >> 8) & 3)
        buf[9] = 512 & 255
        buf[10] = (4 << 2) | ((a_int >> 8) & 3)
        buf[11] = a_int & 255
        buf[12] = (5 << 2) | ((225 >> 8) & 3)
        buf[13] = 225 & 255
        buf[14] = (6 << 2) | ((0 >> 8) & 3)
        buf[15] = 0 & 255
    
        uart.write(buf)
        #print(buf)
        
        ledDisplay()
        battery_read()
        
        sleep(50)
    else:
        print("No Incoming Data")
