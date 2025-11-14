from machine import Pin, PWM
import utime
import math

MID = 1500000
MIN = 1000000
MAX = 2000000

pwm = PWM(Pin(14))
pwm.freq(50)

def smooth_move_variable(start_ns, end_ns, duration=3.0):
    """Variable speed - slower at start/end, faster in middle"""
    steps = 80
    step_delay_base = duration / steps
    
    for i in range(steps + 1):
        t = i / steps
        # Slow start and slow end (ease in-out)
        if t < 0.5:
            ease_t = 2 * t * t  # Accelerate
        else:
            ease_t = 1 - pow(-2 * t + 2, 2) / 2  # Decelerate
            
        current_pos = int(start_ns + (end_ns - start_ns) * ease_t)
        pwm.duty_ns(current_pos)
        
        # Variable delay for smoother motion
        current_delay = step_delay_base * (1.5 if t < 0.2 or t > 0.8 else 0.8)
        utime.sleep(current_delay)
    
    pwm.duty_ns(end_ns)

while True:
    smooth_move_variable(MIN, MID, duration=4.0)
    utime.sleep(1)
    smooth_move_variable(MID, MAX, duration=4.0)
    utime.sleep(1)
    smooth_move_variable(MAX, MID, duration=4.0)
    utime.sleep(1)