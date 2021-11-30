from microbit import * # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime

radio.on() # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=49) 

pitch = 0
arm = 0
roll = 0
throttle = 0
yaw = 0

pixel_y = 4
pr_pixel_x = 1
pr_pixel_y = 1

total_battery: float = 0

throttle_flag = 0

# use LEDs on controller to track throttle, arm, pitch and roll values
def ledDisplay():
    # Arm
    if arm == 1:
        display.set_pixel(0,0,9)
    else:
        display.set_pixel(0,0,0)
    
    # Throttle
    # Pixel position moves as the throttle number increases
    global pixel_y
    old_pixel_y = pixel_y
    display.set_pixel(0, old_pixel_y, 0) # To clear old pixel
    
    if throttle < 25:
        pixel_y = 4
    elif throttle < 50:
        pixel_y = 3
    elif throttle < 75:
        pixel_y = 2
    else:
        pixel_y = 1
        
    display.set_pixel(0, pixel_y, 9)
    
    # Pitch and Roll
    global pr_pixel_x, pr_pixel_y
    old_pr_pixel_x = pr_pixel_x
    old_pr_pixel_y = pr_pixel_y
    display.set_pixel(old_pr_pixel_x, old_pr_pixel_y, 0) # To clear old pixel
    
    if roll == -20: 
        pr_pixel_x = 0 #left
    elif roll == -5:
        pr_pixel_x = 1
    elif roll == 0:
        pr_pixel_x = 2
    elif roll == 5:
        pr_pixel_x = 3
    else:
        pr_pixel_x = 4 #right
    
    if pitch == 20: #forward
        pr_pixel_y = 0
    elif pitch == 5:
        pr_pixel_y = 1
    elif pitch == 0:
        pr_pixel_y = 2
    elif pitch == -5:
        pr_pixel_y = 3
    else:
        pr_pixel_y = 4 #backward
    display.set_pixel(pr_pixel_x, pr_pixel_y, 9)
    
    
while True:
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
            throttle = 0 #Need this here
        else:
            arm = 0
            throttle = 0 #Need this here (tested and this works best)
    
    if button_a.is_pressed() and throttle >= 1: # Min value of throttle is 0
        throttle -= 1
        
    if button_b.is_pressed() and throttle <= 90: # Max value of throttle is 100
        throttle += 1
        
	
    axis_y = -accelerometer.get_y()
    axis_x = accelerometer.get_x()
    print(axis_y)
    if axis_x > 300:
        roll = 20 
    elif axis_x > 150:
        roll = 5
    elif axis_x > -150:
        roll = 0
    elif axis_x > -300:
        roll = -5
    else:
        roll = -20

    if axis_y > 300:
        pitch = 20
    elif axis_y > 150:
        pitch = 5
    elif axis_y > -150:
        pitch = 0
    elif axis_y > -300:
        pitch = -5
    else:
        pitch = -20
 
    # shake command
    if accelerometer.is_gesture("shake"):
        arm = 0
        throttle = 0
    
    ledDisplay()
    radio.send("0" + "," + "0" + "," + str(pitch) + "," + str(roll) + "," + str(throttle) + "," + str(arm))
    sleep(50) 
