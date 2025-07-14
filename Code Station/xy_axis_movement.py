#xy axis servo movement

from machine import Pin, PWM
import time

# Y-axis servo on GP15
servo_y = PWM(Pin(15))
servo_y.freq(50)

# X-axis servo on GP14
servo_x = PWM(Pin(14))
servo_x.freq(50)

def set_angle(servo, angle):
    angle = max(0, min(180, angle))
    duty_ns = int(500000 + (angle / 180) * 2000000)
    servo.duty_ns(duty_ns)

# Let USB and servos settle
time.sleep(2)

# Test sequence
while True:
    # Y: Center → Down → Up → Center
    set_angle(servo_y, 90)
    time.sleep(0.5)
    set_angle(servo_y, 40)
    time.sleep(0.5)
    set_angle(servo_y, 150)
    time.sleep(0.5)
    set_angle(servo_y, 90)
    time.sleep(0.5)

    # X: Center → Left → Right → Center
    set_angle(servo_x, 90)
    time.sleep(0.5)
    set_angle(servo_x, 40)
    time.sleep(0.5)
    set_angle(servo_x, 150)
    time.sleep(0.5)
    set_angle(servo_x, 90)
    time.sleep(0.5)
