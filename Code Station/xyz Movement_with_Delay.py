from machine import Pin, PWM
import time

# === Setup PWM for each servo ===
servo_y = PWM(Pin(15))  # Y-axis
servo_x = PWM(Pin(14))  # X-axis
servo_z = PWM(Pin(13))  # Z-axis

for s in (servo_y, servo_x, servo_z):
    s.freq(50)

# === General smooth movement (for Y and Z axes using 165° scaling) ===
def smooth_move(servo, start, end, delay=0.05, step=1):
    if start < end:
        for angle in range(start, end + 1, step):
            duty_ns = int(500_000 + (angle / 165) * 2_000_000)
            servo.duty_ns(duty_ns)
            time.sleep(delay)
    else:
        for angle in range(start, end - 1, -step):
            duty_ns = int(500_000 + (angle / 165) * 2_000_000)
            servo.duty_ns(duty_ns)
            time.sleep(delay)

# === X-axis smooth movement (uses 180° scaling for gentler motion) ===
def smooth_move_x(servo, start, end, delay=0.07, step=1):
    if start < end:
        for angle in range(start, end + 1, step):
            duty_ns = int(500_000 + (angle / 180) * 2_000_000)
            servo.duty_ns(duty_ns)
            time.sleep(delay)
    else:
        for angle in range(start, end - 1, -step):
            duty_ns = int(500_000 + (angle / 180) * 2_000_000)
            servo.duty_ns(duty_ns)
            time.sleep(delay)

# === Initial neutral position ===
y_current = 90
x_current = 80
z_current = 90

# Smooth startup to avoid jerk at boot
smooth_move(servo_y, 90, y_current)
smooth_move_x(servo_x, 80, x_current)
smooth_move(servo_z, 90, z_current)
time.sleep(1)

# === Main loop with smooth transitions ===
while True:
    # Y-axis: 90 → 80 → 130 → 90
    smooth_move(servo_y, y_current, 80)
    y_current = 80
    time.sleep(0.1)

    smooth_move(servo_y, y_current, 130)
    y_current = 130
    time.sleep(0.1)

    smooth_move(servo_y, y_current, 90)
    y_current = 90
    time.sleep(0.1)

    # X-axis: 80 → 65 → 110 → 80
    smooth_move_x(servo_x, x_current, 65)
    x_current = 65
    time.sleep(0.1)

    smooth_move_x(servo_x, x_current, 110)
    x_current = 110
    time.sleep(0.1)

    smooth_move_x(servo_x, x_current, 80)
    x_current = 80
    time.sleep(0.1)

    # Z-axis: 90 → 70 → 110 → 90
    smooth_move(servo_z, z_current, 70)
    z_current = 70
    time.sleep(0.1)

    smooth_move(servo_z, z_current, 110)
    z_current = 110
    time.sleep(0.1)

    smooth_move(servo_z, z_current, 90)
    z_current = 90
    time.sleep(0.5)
