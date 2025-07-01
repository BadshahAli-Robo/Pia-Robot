#Pia Head Movement
from machine import Pin, PWM
import utime

servo = PWM(Pin(15))
servo.freq(50)

def move_servo_ns(position_ns, delay=1):
    servo.duty_ns(position_ns)
    utime.sleep(delay)

# Head movement positions
LEFT = 2000000   # Right-turn (physical direction depends on mounting)
CENTER = 1500000
RIGHT = 1000000  # Left-turn

while True:
    move_servo_ns(LEFT)     # Look right
    move_servo_ns(CENTER)   # Look center
    move_servo_ns(RIGHT)    # Look left
    move_servo_ns(CENTER)   # Back to center
