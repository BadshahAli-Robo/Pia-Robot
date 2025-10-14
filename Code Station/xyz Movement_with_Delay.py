from machine import Pin, PWM
import time

# === Setup PWM for each servo ===
servo_y = PWM(Pin(15))  # Y-axis (vertical tilt)
servo_x = PWM(Pin(14))  # X-axis (side-to-side)
servo_z = PWM(Pin(13))  # Z-axis (head/neck twist)

for s in (servo_y, servo_x, servo_z):
    s.freq(50)

# === Convert angle (0-180) to PWM duty in nanoseconds ===
def set_angle(servo, angle):
    angle = max(0, min(180, angle))
    duty_ns = int(500_000 + (angle / 180) * 2_000_000)
    servo.duty_ns(duty_ns)

# === Smooth motion function ===
def smooth_move(servo, start, end, delay=0.1, step=1):
    if start < end:
        for angle in range(start, end + 1, step):
            set_angle(servo, angle)
            time.sleep(delay)
    else:
        for angle in range(start, end - 1, -step):
            set_angle(servo, angle)
            time.sleep(delay)

# === Let system stabilize ===
time.sleep(1)

# === Initial angles ===
y_current = 90
x_current = 90
z_current = 90
set_angle(servo_y, y_current)
set_angle(servo_x, x_current)
set_angle(servo_z, z_current)
time.sleep(1)

# === Movement loop ===
while True:
    # Move Y axis: 90 -> 60 -> 120 -> 90
    smooth_move(servo_y, y_current, 80, delay=0.04)
    y_current = 80
    smooth_move(servo_y, y_current, 110, delay=0.04)
    y_current = 110
    smooth_move(servo_y, y_current, 90, delay=0.04)
    y_current = 90

    # Move X axis: 90 -> 70 -> 120 -> 90
    smooth_move(servo_x, x_current, 70, delay=0.04)
    x_current = 70
    smooth_move(servo_x, x_current, 120, delay=0.04)
    x_current = 120
    smooth_move(servo_x, x_current, 90, delay=0.04)
    x_current = 90

    # Move Z axis: 90 -> 0 -> 180 -> 90
    smooth_move(servo_z, z_current, 0, delay=0.04)
    z_current = 0
    smooth_move(servo_z, z_current, 180, delay=0.04)
    z_current = 180
    smooth_move(servo_z, z_current, 90, delay=0.04)
    z_current = 90

    # Optional pause at end of full cycle
    time.sleep(0.5)
