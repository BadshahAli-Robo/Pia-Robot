from machine import Pin, PWM
import utime
import math

MID = 1500000
MIN = 1000000
MAX = 2000000

pwm = PWM(Pin(14))
pwm.freq(50)

current_position = MID

def super_smooth_move(target_ns, duration=5.0):
    """
    Super smooth movement with consistent easing
    """
    global current_position
    
    start_ns = current_position
    if start_ns == target_ns:
        return
    
    print(f"Moving: {start_ns} → {target_ns}")
    
    # Consistent timing for all movements
    update_interval = 0.015  # 15ms - optimal for smoothness
    total_updates = int(duration / update_interval)
    
    for i in range(total_updates + 1):
        t = i / total_updates
        
        # **Consistent cubic easing for all movements**
        ease_t = t * t * (3 - 2 * t)  # Perfect balance of smoothness
        
        current_pos = int(start_ns + (target_ns - start_ns) * ease_t)
        pwm.duty_ns(current_pos)
        utime.sleep(update_interval)
    
    current_position = target_ns

def emergency_return_to_center():
    """Call this anytime to smoothly return to center"""
    global current_position
    print("EMERGENCY: Returning to center...")
    super_smooth_move(MID, duration=4.0)
    print("Safe at center position!")

# Initialize
pwm.duty_ns(MID)
current_position = MID
utime.sleep(1)
print("Ready! Press Ctrl+C to safely return to center.")

try:
    while True:
        # Perfectly smooth cycle
        super_smooth_move(MIN, duration=6.0)
        utime.sleep(0.3)
        
        super_smooth_move(MID, duration=6.0) 
        utime.sleep(0.3)
        
        super_smooth_move(MAX, duration=6.0)
        utime.sleep(0.3)
        
        super_smooth_move(MID, duration=6.0)
        utime.sleep(1.0)
        
except KeyboardInterrupt:
    emergency_return_to_center()
except Exception as e:
    print(f"Error: {e}")
    emergency_return_to_center()