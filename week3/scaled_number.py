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
flight_mode = 45
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

def scaleTheNumbers(string_letter):
    # To-do: Flight mode is going to be 45. Add this into the logic
    if(string_letter == 'P'):
        p = int(pitch * 3.5 + 512)
        return int(p)
    elif(string_letter == 'A'):
        a = 180*5
        return a
    elif(string_letter == 'R'):
        r = int(roll * 3.5 + 521)
        return int(r)
    elif(string_letter == 'T'):
        t = int(throttle) * 512 / 50
        return int(t)
    elif(string_letter == 'Y'):
       # To-Do: Add Yaw logic



while True:
    incoming = str(radio.receive())

    if (incoming != 'None'): # If a message is incoming
        split_string = incoming.split("_")
        display.show(Image.HEART)

        if (split_string[0] == 'P'):
            pitch = split_string[1]

        elif (split_string[0] == 'A'):
            arm = split_string[1]

        elif (split_string[0] == 'R'):
            roll = split_string[1]
            #print(roll)

        elif (split_string[0] == 'T'):
            throttle = split_string[1]

        else:
            print('error')



        sleep(100)

    else:
        display.show(Image.SKULL)
        #display.scroll(throttle)
        display.scroll(arm)
        sleep(100)

    # Scale and offset values
    p_int = scaleTheNumbers('P')
    if (arm != 0):
        scaleTheNumbers('A')
    r_int = scaleTheNumbers('R')
    t_int = scaleTheNumbers('T')

    # parse into buffer
    buf[0] = 0
    buf[1] = 0x01

    if (r_int > 255):
        buf[2] = (r_int >> 8) and 255
        buf[3] = r_int and 255
    else:
        buf[2] = (roll_id << 2) and 255
        buf[3] = r_int and 255

    if (p_int > 255):
        buf[4] = p_int >> 8 and 255
        buf[5] = p_int and 255
    else:
        buf[4] = pitch_id << 2 and 255
        buf[5] = p_int and 255

    if (t_int > 255):
        buf[6] = t_int >> 8 and 255
        buf[7] = t_int and 255
    else:
        buf[6] = throttle_id << 2 and 255
        buf[7] = t_int and 255

    if (yaw > 255):
        buf[8] = yaw >> 8 and 255
        buf[9] = yaw and 255
    else:
        buf[8] = yaw_id << 2 and 255
        buf[9] = yaw and 255

    if (a > 255):
        #print(a)
        buf[10] = a >> 8 and 255
        buf[11] = a and 255
    else:
        #print(a)
        buf[10] = a << 2 and 255
        buf[11] = a and 255

    buf[12] = fm_id << 2 and 255
    buf[13] = flight_mode and 255
    buf[14] = buzzer_id << 2 and 255
    buf[15] = buzzer and 255

    #print(buf)

    uart.write(buf)
    #print(by)

