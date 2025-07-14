#DF9GMS Servos Code#02

#we gave usb time to settle

from machine import Pin, PWM
import time

servo_y = PWM(Pin(13))
servo_y.freq(50)  # 50Hz for standard servo timing

def set_angle(angle):
    # Clamp angle to 0–180
    angle = max(0, min(180, angle))
    # Convert angle to duty_ns (0.5ms–2.5ms = 500000–2500000 ns)
    duty_ns = int(500000 + (angle / 180) * 2000000)
    servo_y.duty_ns(duty_ns)
time.sleep(2)
# Test movement: 90° → 0° → 180° → 90°
while True:
    set_angle(90)
    time.sleep(1)
    set_angle(0)
    time.sleep(1)
    set_angle(180)
    time.sleep(1)
    set_angle(90)
    time.sleep(1)


