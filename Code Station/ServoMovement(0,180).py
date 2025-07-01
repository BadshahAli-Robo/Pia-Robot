from machine import Pin, PWM
import time

servo = PWM(Pin(15))
servo.freq(50)

def spin_cw(duration=0.4):  # Clockwise for a short time
    servo.duty_ns(2000000)
    time.sleep(duration)
    servo.duty_ns(1500000)  # Stop

def spin_ccw(duration=0.4):  # Counter-clockwise
    servo.duty_ns(1000000)
    time.sleep(duration)
    servo.duty_ns(1500000)  # Stop

while True:
    spin_ccw()  # Simulate “look left”
    time.sleep(1)
    spin_cw()   # Simulate “look right”
    time.sleep(1)
