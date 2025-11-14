from machine import Pin, PWM
import utime

MID = 1500000
MIN = 1000000
MAX = 2000000

pwm = PWM(Pin(14))
pwm.freq(50)

def continuous_sweep(start_ns, end_ns, duration=4.0):
    """Continuous sweep without discrete steps"""
    # Set initial position
    pwm.duty_ns(start_ns)
    utime.sleep(0.1)
    
    # Calculate the total change needed
    total_change = end_ns - start_ns
    update_interval = 0.01  # 20ms updates
    total_updates = int(duration / update_interval)
    change_per_update = total_change / total_updates
    
    # Continuous update
    current = start_ns
    for _ in range(total_updates):
        current += change_per_update
        pwm.duty_ns(int(current))
        utime.sleep(update_interval)
    
    pwm.duty_ns(end_ns)

while True:
    print("MIN to MID")
    continuous_sweep(MIN, MID, duration=6.0)
    utime.sleep(1)
    
    print("MID to MAX")
    continuous_sweep(MID, MAX, duration=5.0)
    utime.sleep(1)
    
    print("MAX to MID")
    continuous_sweep(MAX, MID, duration=6.0)
    utime.sleep(1)