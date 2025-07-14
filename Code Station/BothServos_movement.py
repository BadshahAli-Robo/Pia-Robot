#coordinating both servo together 

from machine import Pin, PWM
import time

servo_y = PWM(Pin(15))
servo_y.freq(50)

servo_x = PWM(Pin(14))
servo_x.freq(50)

def set_angle(servo, angle):
    angle = max(0, min(180, angle))
    duty_ns = int(500000 + (angle / 180) * 2000000)
    servo.duty_ns(duty_ns)

time.sleep(2)  # Let things settle

while True:
    # Move both to center
    set_angle(servo_y, 90)
    set_angle(servo_x, 90)
    time.sleep(0.5)

#     # Move both to left/down
#     set_angle(servo_y, 50)
#     set_angle(servo_x, 50)
#     time.sleep(0.5)
# 
#     # Move both to right/up
#     set_angle(servo_y, 150)
#     set_angle(servo_x, 150)
#     time.sleep(0.5)
# 
#     # Return both to center
#     set_angle(servo_y, 90)
#     set_angle(servo_x, 90)
#     time.sleep(0.5)
#     
#     set_angle(servo_y, 50)   # tilt head slightly down
#     set_angle(servo_x, 150)  # rotate to one side
#     time.sleep(0.5)

