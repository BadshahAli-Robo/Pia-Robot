#this is kinda accurate, but the x & y axis move so fast that it cause jitter and the z-axis can't excute. 


from machine import Pin, PWM
import time

# Setup PWM for each axis
servo_y = PWM(Pin(15))  # Y-axis
servo_x = PWM(Pin(14))  # X-axis
servo_z = PWM(Pin(13))  # Z-axis

# Set frequency for all
for servo in [servo_y, servo_x, servo_z]:
    servo.freq(50)

def set_angle(servo, angle):
#     """Set angle (0–180°) safely using duty_ns."""
    angle = max(0, min(180, angle))
    duty_ns = int(500000 + (angle / 180) * 2000000)
    servo.duty_ns(duty_ns)

# Custom angle limits
MIN_ANGLE = 40
MAX_ANGLE = 150
CENTER = 90

# Let USB and servos stabilize
time.sleep(2)

try:
    while True:
        # Move all servos to center
        set_angle(servo_y, CENTER)
        set_angle(servo_x, CENTER)
        set_angle(servo_z, CENTER)
        time.sleep(0.5)

        # Y-axis (tilt): center → min → max → center
        set_angle(servo_y, MIN_ANGLE)
        time.sleep(0.5)
        set_angle(servo_y, MAX_ANGLE)
        time.sleep(0.5)
        set_angle(servo_y, CENTER)
        time.sleep(0.5)

        # X-axis (rotation): center → min → max → center
        set_angle(servo_x, MIN_ANGLE)
        time.sleep(0.5)
        set_angle(servo_x, MAX_ANGLE)
        time.sleep(0.5)
        set_angle(servo_x, CENTER)
        time.sleep(0.5)

        # Z-axis (gesture): center → min → max → center
        set_angle(servo_z, MIN_ANGLE)
        time.sleep(0.5)
        set_angle(servo_z, MAX_ANGLE)
        time.sleep(0.5)
        set_angle(servo_z, CENTER)
        time.sleep(0.5)

except Exception as e:
    print("Error:", e)

    # Safely disable PWM to stop all movement
    for servo in [servo_y, servo_x, servo_z]:
        servo.deinit()

    print("PWM signals stopped. Reset board if needed.")
