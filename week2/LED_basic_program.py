from microbit import *
# Each LED pixel on the physical display can be set to one of ten values. 
# If a pixel is set to 0 (zero) then it’s off. It literally has zero brightness. 
# However, if it is set to 9 then it is at its brightest level. 
# The values 1 to 8 represent the brightness levels between off (0) and full on (9).
throttle = 0
pixel_x = 4
while True:
    # sets the brightness of the pixel (x,y) to val (between 0 [off] and 9 [max
    # brightness], inclusive).
    
    display.set_pixel(0, 0, 1)
    display.set_pixel(0, 1, 9)
    
    # To remove the old pixel_x pixel from the LED display
    old_pixel_x = pixel_x
    display.set_pixel(old_pixel_x, 0, 0)
    
    # Example of using the pixel to show a value of a variable
    # Pixel position moves as the throttle number increases
    throttle += 5
    if throttle < 25:
        pixel_x = 1
    elif throttle < 50:
        pixel_x = 2
    elif throttle < 75:
        pixel_x = 3
    else:
        pixel_x = 4
        throttle = 0
    display.set_pixel(pixel_x, 0, 8)
    sleep(2000)
