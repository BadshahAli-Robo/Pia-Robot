import machine
import time
import math

# Servo setup with power management
servo_y = machine.PWM(machine.Pin(15))
servo_x = machine.PWM(machine.Pin(14))
servo_z = machine.PWM(machine.Pin(13))

servo_y.freq(50)
servo_x.freq(50)
servo_z.freq(50)

# Conservative calibration for DF9GMS
SERVO_MIN_US = 600
SERVO_MAX_US = 2400
SERVO_MIN_DUTY = int((SERVO_MIN_US * 65535) / 20000)
SERVO_MAX_DUTY = int((SERVO_MAX_US * 65535) / 20000)

# Initial positions
current_y = 90
current_x = 80
current_z = 90

# Power stabilization
time.sleep(1)
print("Power stabilized")

def angle_to_duty(angle):
    angle = max(0, min(180, angle))
    pulse_width = SERVO_MIN_US + (angle / 180) * (SERVO_MAX_US - SERVO_MIN_US)
    duty = int((pulse_width * 65535) / 20000)
    return max(SERVO_MIN_DUTY, min(SERVO_MAX_DUTY, duty))

def set_servo_ultra_smooth(servo, current_angle, target_angle, duration=3.0):
    """Ultra smooth movement with cosine easing"""
    if current_angle == target_angle:
        return target_angle
        
    steps = 150  # More steps for smoother movement
    step_delay = duration / steps
    
    for i in range(steps + 1):
        t = i / steps
        # Cosine easing for very smooth movement
        smooth_t = 0.5 - 0.5 * math.cos(t * math.pi)
        
        intermediate_angle = current_angle + (target_angle - current_angle) * smooth_t
        servo.duty_u16(angle_to_duty(intermediate_angle))
        time.sleep(step_delay)
    
    return target_angle

def move_y_sequence():
    global current_y
    print("Y servo moving...")
    current_y = set_servo_ultra_smooth(servo_y, current_y, 80, 3.0)
    time.sleep(1)
    current_y = set_servo_ultra_smooth(servo_y, current_y, 120, 3.0)
    time.sleep(1)
    current_y = set_servo_ultra_smooth(servo_y, current_y, 90, 3.0)
    time.sleep(1)

def move_x_sequence():
    global current_x
    time.sleep(0.3)  # Power recovery delay
    print("X servo moving...")
    current_x = set_servo_ultra_smooth(servo_x, current_x, 65, 3.0)
    time.sleep(1)
    current_x = set_servo_ultra_smooth(servo_x, current_x, 110, 3.0)
    time.sleep(1)
    current_x = set_servo_ultra_smooth(servo_x, current_x, 80, 3.0)
    time.sleep(1)

def move_z_sequence():
    global current_z
    time.sleep(0.3)  # Power recovery delay
    print("Z servo moving...")
    current_z = set_servo_ultra_smooth(servo_z, current_z, 70, 3.0)
    time.sleep(1)
    current_z = set_servo_ultra_smooth(servo_z, current_z, 110, 3.0)
    time.sleep(1)
    current_z = set_servo_ultra_smooth(servo_z, current_z, 90, 3.0)
    time.sleep(1)

# Initialize
servo_y.duty_u16(angle_to_duty(current_y))
servo_x.duty_u16(angle_to_duty(current_x))
servo_z.duty_u16(angle_to_duty(current_z))
time.sleep(1)

try:
    while True:
        move_y_sequence()
        move_x_sequence()
        move_z_sequence()
except KeyboardInterrupt:
    print("Returning home...")
    # Smooth return to initial positions
    set_servo_ultra_smooth(servo_y, current_y, 90, 4.0)
    set_servo_ultra_smooth(servo_x, current_x, 80, 4.0)
    set_servo_ultra_smooth(servo_z, current_z, 90, 4.0)