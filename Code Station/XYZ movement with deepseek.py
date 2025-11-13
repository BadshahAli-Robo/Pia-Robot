import machine
import time
from math import sin, pi

# Servo setup
servo_y = machine.PWM(machine.Pin(15))  # Y-axis
servo_x = machine.PWM(machine.Pin(14))  # X-axis
servo_z = machine.PWM(machine.Pin(13))  # Z-axis

# Set PWM frequency for servos (50Hz standard for servos)
servo_y.freq(50)
servo_x.freq(50)
servo_z.freq(50)

# Servo calibration (adjust these values for your specific servos)
SERVO_MIN_US = 500   # Minimum pulse width in microseconds
SERVO_MAX_US = 2500  # Maximum pulse width in microseconds
SERVO_MIN_DUTY = int((SERVO_MIN_US * 65535) / 20000)  # Convert to duty cycle
SERVO_MAX_DUTY = int((SERVO_MAX_US * 65535) / 20000)  # Convert to duty cycle

# Initial positions
INITIAL_Y = 90
INITIAL_X = 80
INITIAL_Z = 90

# Current positions (for tracking)
current_y = INITIAL_Y
current_x = INITIAL_X
current_z = INITIAL_Z

def angle_to_duty(angle):
    """Convert angle (0-180) to PWM duty cycle"""
    angle = max(0, min(180, angle))  # Clamp angle to valid range
    pulse_width = SERVO_MIN_US + (angle / 180) * (SERVO_MAX_US - SERVO_MIN_US)
    duty = int((pulse_width * 65535) / 20000)
    return max(SERVO_MIN_DUTY, min(SERVO_MAX_DUTY, duty))

def set_servo_smooth(servo, current_angle, target_angle, duration=1.0, steps=50):
    """Move servo smoothly from current angle to target angle"""
    step_delay = duration / steps
    
    for i in range(steps + 1):
        # Ease in-out function for smooth movement
        t = i / steps
        # Smooth step (ease in-out)
        smooth_t = t * t * (3 - 2 * t)
        
        # Calculate intermediate angle
        intermediate_angle = current_angle + (target_angle - current_angle) * smooth_t
        
        # Set servo position
        servo.duty_u16(angle_to_duty(intermediate_angle))
        time.sleep(step_delay)
    
    return target_angle  # Return new current position

def move_y_sequence():
    """Y servo movement sequence"""
    global current_y
    print("Moving Y servo...")
    
    # 90° to 80°
    current_y = set_servo_smooth(servo_y, current_y, 80, duration=1.0)
    time.sleep(1)
    
    # 80° to 120°
    current_y = set_servo_smooth(servo_y, current_y, 120, duration=1.0)
    time.sleep(1)
    
    # 120° to 90°
    current_y = set_servo_smooth(servo_y, current_y, 90, duration=1.0)
    time.sleep(1)

def move_x_sequence():
    """X servo movement sequence"""
    global current_x
    print("Moving X servo...")
    
    # 80° to 65°
    current_x = set_servo_smooth(servo_x, current_x, 65, duration=1.0)
    time.sleep(1)
    
    # 65° to 110°
    current_x = set_servo_smooth(servo_x, current_x, 110, duration=1.0)
    time.sleep(1)
    
    # 110° to 80°
    current_x = set_servo_smooth(servo_x, current_x, 80, duration=1.0)
    time.sleep(1)

def move_z_sequence():
    """Z servo movement sequence"""
    global current_z
    print("Moving Z servo...")
    
    # 90° to 70°
    current_z = set_servo_smooth(servo_z, current_z, 70, duration=1.0)
    time.sleep(1)
    
    # 70° to 110°
    current_z = set_servo_smooth(servo_z, current_z, 110, duration=1.0)
    time.sleep(1)
    
    # 110° to 90°
    current_z = set_servo_smooth(servo_z, current_z, 90, duration=1.0)
    time.sleep(1)

def return_to_initial():
    """Smoothly return all servos to initial positions"""
    global current_y, current_x, current_z
    print("Returning to initial positions...")
    
    # Move all servos to initial positions simultaneously for efficiency
    # You can also move them sequentially if preferred
    
    # Move Y to 90°
    current_y = set_servo_smooth(servo_y, current_y, INITIAL_Y, duration=2.0)
    
    # Move X to 80°
    current_x = set_servo_smooth(servo_x, current_x, INITIAL_X, duration=2.0)
    
    # Move Z to 90°
    current_z = set_servo_smooth(servo_z, current_z, INITIAL_Z, duration=2.0)
    
    print("All servos returned to initial positions")

def main_sequence():
    """Main movement sequence"""
    try:
        while True:
            move_y_sequence()
            move_x_sequence()
            move_z_sequence()
            
    except KeyboardInterrupt:
        print("Sequence interrupted")
        return_to_initial()

# Initialize servos to current positions on startup
def initialize_servos():
    """Set servos to their current positions on startup"""
    print("Initializing servos...")
    servo_y.duty_u16(angle_to_duty(current_y))
    servo_x.duty_u16(angle_to_duty(current_x))
    servo_z.duty_u16(angle_to_duty(current_z))
    time.sleep(0.5)

# Run initialization
initialize_servos()

# You can choose to either run the main sequence or return to initial positions
# Option 1: Run the main movement sequence
print("Starting main movement sequence...")
main_sequence()

# Option 2: If you want to only return to initial positions and stop:
# return_to_initial()
# print("Ready for new commands")