from machine import Pin, time_pulse_us, PWM
import hc_sr04_edushields
import time

ENA1 = Pin(10, Pin.OUT)  # Enable pin1
IN1 = Pin(11, Pin.OUT)  # IN1 pin
IN2 = Pin(12, Pin.OUT)  # IN2 pin

ENA2 = Pin(21, Pin.OUT)  # Enable pin2
IN3 = Pin(20, Pin.OUT)  # IN3 pin
IN4 = Pin(19, Pin.OUT)  # IN4 pin

# define pins
S0 = Pin(6, Pin.OUT)
S1 = Pin(7, Pin.OUT)
S2 = Pin(8, Pin.OUT)
S3 = Pin(9, Pin.OUT)
signal = Pin(5, Pin.IN)
button = Pin(22, Pin.IN)
# Pin configuration
USON_TRIGGER_GP_NUM = 1
USON_ECHO_GP_NUM    = 1
SPEAKER_GP_NUM = 18

# Initialize ultrasonic sensor and speaker
usonic = hc_sr04_edushields.HCSR04(USON_TRIGGER_GP_NUM, USON_ECHO_GP_NUM)
speaker = PWM(Pin(SPEAKER_GP_NUM))

# Constants
PWM_MAX = (2**16) - 1
MIN_DIST = 20  # mm
MAX_DIST = 500  # mm
MIN_FREQ = 200  # Hz
MAX_FREQ = 4000  # Hz

def distance_to_frequency(distance_mm):
    # Apply the formula and cap the frequencies
    if distance_mm < MIN_DIST:
        return MAX_FREQ
    elif distance_mm > MAX_DIST:
        return MIN_FREQ
    else:
        # Linear interpolation formula
        return -7.9167 * distance_mm + 4158.334

# function to read frequency from the sensor
def read_color_filter(s2_val, s3_val):
    S2.value(s2_val)
    S3.value(s3_val)
    pulse_time = time_pulse_us(signal, 1, 10000)  # measure pulse width in microseconds
    return pulse_time if pulse_time > 0 else 10000  # handle timeout

power = 0;
state = 1;

def check_color_sensor():
    # read clear filter
    clear = read_color_filter(1, 0)

    # read red filter
    r = 0;
    i = 0;
    while i < 6:
        r += read_color_filter(0, 0)
        i += 1;
        if r > 9000:
            i = 0;
            r = 0;
    red = r / 6;    
    #red = read_color_filter(0, 0)

    # read green filter
    g = 0;
    i = 0;
    while i < 6:
        g += read_color_filter(1, 1)
        i += 1;
        if g > 9000:
            i = 0;
            g = 0;
    green = g / 6; 

    # read blue filter
    b = 0;
    i = 0;
    while i < 6:
        b += read_color_filter(0, 1)
        i += 1;
        if b > 9000:
            i = 0;
            b = 0;
    blue = b / 6; 

    # map the red, green, and blue values to a more intuitive 0-255 range
    red = int((147 - red) * 255 / 147)
    green = int((147 - green) * 255 / 147)
    blue = int((147 - blue) * 255 / 147)
    print(f"Red: {red} | Green: {green} | Blue: {blue}")
    
    global state;
    #set car behavioral state
    if red > 170 and blue < 140 and green < 140:
        #motor_halt()  # Stop the car if red is detected
        state = 0;
        print("Red detected - Stop!")
    elif red < 150 and blue > 120 and green < 120:
        #motor_left()  # Turn left if blue is detected
        state = 9;
        print("Blue detected - Left!")
    elif red < 150 and blue < 140 and green > 120:
        #motor_rght()  # Turn right if green is detected
        state = 3;
        print("Green detected - Right!")
    elif red > 200 and blue > 200 and green > 200:
        state = 0;
    else:
        state = 1;
   # print(signal.value())

# setup
S0.value(1)  # HIGH
S1.value(0)  # LOW (20% frequency scaling)

# Start the motor
def motor_move():
    ENA1.value(1)  # Enable motor
    IN1.value(1)  # Set IN1 to high (turn on motor)
    IN2.value(0)  # Set IN2 to low (motor runs in one direction
    ENA2.value(1)  # Enable motor
    IN3.value(1)  # Set IN1 to high (turn on motor)
    IN4.value(0)  # Set IN2 to low (motor runs in one direction

# Stop the motor
def motor_halt():
    ENA1.value(0)  
    IN1.value(0)  
    IN2.value(0)  
    ENA2.value(0)  
    IN3.value(0)  
    IN4.value(0)  
    
# Reverse motor
def motor_back():
    ENA1.value(1)  
    IN1.value(0) 
    IN2.value(1)  
    ENA2.value(1)  
    IN3.value(0) 
    IN4.value(1)  
    
    
# Right turn
def motor_rght():
    ENA1.value(1)  
    IN1.value(1)  
    IN2.value(0)  
    ENA2.value(1)  
    IN3.value(0)  
    IN4.value(1)  
    
# Left turn
def motor_left():
    ENA1.value(1)  
    IN1.value(0)  
    IN2.value(1)  
    ENA2.value(1)  
    IN3.value(1)  
    IN4.value(0)  


# Run the motor on for 5 seconds and off for 3 seconds
while True:
    # print readings
    #print(button.value())
    check_color_sensor()
    
    #print(button.value())
    if (not button.value()):
        power = not power
        print(power)
        time.sleep(1)
    #state = state*power
    
    dist = usonic.range_mm()
    print(dist)
    
    time.sleep(0.05)
    if state == (0):
        motor_halt()
    elif state == (9):
        motor_left()
    elif state == (3):
        motor_rght()
    else:
        if dist < 200 and dist > 0:
            motor_back()
            time.sleep(0.5)
            motor_rght()
        else:
            motor_move()
    #print(state);
    time.sleep(0.45)
    # Get the distance in mm

    
        
    #time.sleep(1)  # Motor runs for 5 seconds
    #motor_halt()
    #check_color_sensor()
    #time.sleep(1)  # Motor stops for 3 seconds
    #motor_left()
    #check_color_sensor()
    #time.sleep(1)  # Motor runs for 5 seconds
    #motor_back()
    #check_color_sensor()
    #time.sleep(1)  # Motor stops for 3 seconds
    #motor_rght()
    #check_color_sensor()
    #time.sleep(1)  # Motor stops for 3 seconds