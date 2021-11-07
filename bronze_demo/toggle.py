from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

display.off()

p_up = 0
p_down = 0
r_up = 0
r_down = 0

a_prev_state = pin3.read_digital()

while True:
    
    # orange = A
    a = pin3.read_digital()
    # green = B
    b = pin0.read_digital()
    
    print("A: ", a, " B: ", b)
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
    
    a_state = pin3.read_digital()
    #print(a_state, a_prev_state)
    
    if a_state != a_prev_state:
        if pin0.read_digital() != a_state:
            # throttle increasing
            p_up = p_up + 1
            
            if p_up == 24:
                p_up = 0
                r_up = r_up + 1
                
        elif pin0.read_digital() == a_state:
            # throttle decreasing       
            p_down = p_down + 1
        
            if p_down == 24:
                p_down = 0
                r_down = r_down + 1
                
        
        #print(position)    
        
        
    a_prev_state = a_state
    
    print("R up: ", r_up, "|", "R down: ", r_down)
    
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()
    
    print("Pitch: ", pitch, "|", "Roll: ", roll)
    
    radio.send("P_" + str(pitch) + "_R_" + str(roll) + "_T_" + str(r_up))
