# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import time

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)
radio.on()  # Radio won't work unless it's on
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)
micropython.kbd_intr(-1)
incoming = 0
buzzer = 0
arm = ""
yaw = 0


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

    local_throttle = int(throttle)
    if local_throttle < 25:
        pixel_y = 4
    elif local_throttle < 50:
        pixel_y = 3
    elif local_throttle < 75:
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
    
    if r >= 0 and r < 200:
        pr_pixel_x = 0
    elif r > 200 and r < 400:
        pr_pixel_x = 1
    elif r > 400 and r < 600:
        pr_pixel_x = 2
    elif r > 600 and r < 800:
        pr_pixel_x = 3
    elif r > 800 and r <= 1023:
        pr_pixel_x = 4
    
    if p >= 0 and p < 200:
        pr_pixel_y = 4
    elif p > 200 and p < 400:
        pr_pixel_y = 3
    elif p > 400 and p < 600:
        pr_pixel_y = 2
    elif p > 600 and p < 800:
        pr_pixel_y = 1
    elif p > 800 and p <= 1023:
        pr_pixel_y = 0
        
    # values = [-20, -10, 0, 10, 20] # List of roll values
    # # Roll is -20 on LHS and 20 on RHS
    # # Pitch is 20 going forward and -20 going backwards
        
    # for y in values:
    #     if p == y:
    #         # At 20, pixel should be 0, and at -20, pixel should be 4
    #         # Opposit way round to roll
    #         pr_pixel_y = (values.index(y) - 4) * (-1) 
    #         break
  
    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)

# displays % charging on LEDs 
# warns controller if battery charge on drone is less than 20 %
def battery_read():
    battery = pin0.read_analog()
    radio.send("_Battery_" + str(battery))
    
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
    global r_int, arm
    flight_mode = 45 * 5

    p_int = int(pitch) * 3.5 + 512
    p_int = int(p_int)

    if arm == "1":
        a_int = 180 * 5
    else:
        a_int = 0

    # r_int = int(roll) * 3.5 + 521
    # r_int = int(r_int)
    r_int = int(roll)

    t_int = int(throttle) * 512 / 50
    t_int = int(t_int)

    y_int = int(yaw) * 5 + 512
    y_int = int(y_int)
    
    # roll_id = 0
    # pitch_id = 1
    # throttle_id = 2
    # yaw_id = 3
    # arm_id = 4
    # flight_mode_id = 5
    # buzzer_id = 6
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

def telemetry():
    global curr_r
    curr_r = accelerometer.get_x() # roll
    
    global scaled_tele_roll
    scaled_tele_roll = (curr_r*3.5) + 521
    
    
def errorValue():
    error_roll = r_int - scaled_tele_roll
    radio.send("_Roll_"+ str(error_roll))
    
while True:
    
    start = time.ticks_ms();
    incoming = radio.receive()
    
    if incoming:
        receive_data()
        read_into()
        ledDisplay()
        battery_read()
        telemetry()
        errorValue()
        sleep(50)
    else:
        print("No Incoming Data")
    
    end = time.ticks_ms()
    #print("Time Taken: ", end - start);

    
