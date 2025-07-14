from machine import Pin, PWM
import time

# Setup PWM for all three axes
servo_y = PWM(Pin(15))
servo_x = PWM(Pin(14))
servo_z = PWM(Pin(13))

for s in [servo_y, servo_x, servo_z]:
    s.freq(50)

def set_angle(servo, angle):
    angle = max(0, min(180, angle))
    duty_ns = int(500000 + (angle / 180) * 2000000)
    servo.duty_ns(duty_ns)

def smooth_move(servo, start, end, step=2, delay=0.01):
    if start < end:
        angles = range(start, end + 1, step)
    else:
        angles = range(start, end - 1, -step)
    for angle in angles:
        set_angle(servo, angle)
        time.sleep(delay)

# Angle limits
MIN_ANGLE = 40
MAX_ANGLE = 150
CENTER = 90

time.sleep(2)

try:
    while True:
        # Y-axis smooth: center → min → max → center
        smooth_move(servo_y, CENTER, MIN_ANGLE)
        smooth_move(servo_y, MIN_ANGLE, MAX_ANGLE)
        smooth_move(servo_y, MAX_ANGLE, CENTER)

        # X-axis smooth
        smooth_move(servo_x, CENTER, MIN_ANGLE)
        smooth_move(servo_x, MIN_ANGLE, MAX_ANGLE)
        smooth_move(servo_x, MAX_ANGLE, CENTER)

        # Z-axis smooth
        smooth_move(servo_z, CENTER, MIN_ANGLE)
        smooth_move(servo_z, MIN_ANGLE, MAX_ANGLE)
        smooth_move(servo_z, MAX_ANGLE, CENTER)

except Exception as e:
    print("Error:", e)
    for s in [servo_y, servo_x, servo_z]:
        s.deinit()
    print("PWM signals stopped.")
