from machine import Pin, PWM
import utime
import math
from neopixel import NeoPixel

# ==================== NEO-PIXEL SETUP ====================
NEOPIXEL_PIN = 12
NUM_LEDS = 24
np = NeoPixel(Pin(NEOPIXEL_PIN), NUM_LEDS)

# ==================== SERVO CONFIGURATION ====================
class ServoConfig:
    SERVO_RANGE = {'min': 1000000, 'mid': 1500000, 'max': 2000000}
    SERVO_PINS = {'y': 15, 'x': 14, 'z': 13}
    INITIAL_POSITIONS = {'y': 90, 'x': 80, 'z': 90}

# ==================== COMPLETE ROBOT CONTROLLER ====================
class CompleteRobotController:
    def __init__(self):
        # Initialize servos
        self.servos = {}
        self.current_positions = {}
        
        for axis, pin in ServoConfig.SERVO_PINS.items():
            self.servos[axis] = PWM(Pin(pin))
            self.servos[axis].freq(50)
            initial_ns = self._degree_to_ns(ServoConfig.INITIAL_POSITIONS[axis])
            self.current_positions[axis] = initial_ns
            self.servos[axis].duty_ns(initial_ns)
        
        # Start with LEDs off
        self.led_clear()
        print("🤖 Robot Initialized!")
    
    def _degree_to_ns(self, degrees):
        degrees = max(0, min(180, degrees))
        min_ns = ServoConfig.SERVO_RANGE['min']
        max_ns = ServoConfig.SERVO_RANGE['max']
        return int(min_ns + (degrees / 180) * (max_ns - min_ns))
    
    def _ns_to_degree(self, ns):
        min_ns = ServoConfig.SERVO_RANGE['min']
        max_ns = ServoConfig.SERVO_RANGE['max']
        return int((ns - min_ns) / (max_ns - min_ns) * 180)
    
    # ==================== NEO-PIXEL EFFECTS ====================
    def led_clear(self):
        """Turn all LEDs off"""
        for i in range(NUM_LEDS):
            np[i] = (0, 0, 0)
        np.write()
    
    def led_brightness_increase(self, duration=1.5):
        """Quickly increase brightness from 10 to 255"""
        print("💡 Brightness increasing quickly...")
        steps = 20
        for step in range(steps + 1):
            brightness = 10 + int((150 - 10) * (step / steps))
            for i in range(NUM_LEDS):
                np[i] = (brightness, brightness, brightness)
            np.write()
            utime.sleep(duration / steps)
    
    def led_brightness_decrease(self, duration=1.5):
        """Gradually decrease brightness from 255 to 10"""
        print("💡 Brightness decreasing...")
        steps = 20
        for step in range(steps + 1):
            brightness = 150 - int((150 - 10) * (step / steps))
            for i in range(NUM_LEDS):
                np[i] = (brightness, brightness, brightness)
            np.write()
            utime.sleep(duration / steps)
        self.led_clear()
    
    def led_rainbow_effect(self):
        """Quick rainbow effect before movement"""
        print("🌈 Rainbow effect!")
        for cycle in range(2):  # Quick 2 cycles
            for i in range(NUM_LEDS):
                hue = (i * 256 // NUM_LEDS) + (cycle * 20)
                if hue < 85:
                    np[i] = (hue * 3, 255 - hue * 3, 0)
                elif hue < 170:
                    hue -= 85
                    np[i] = (255 - hue * 3, 0, hue * 3)
                else:
                    hue -= 170
                    np[i] = (0, hue * 3, 255 - hue * 3)
            np.write()
            utime.sleep(0.3)
        self.led_clear()
    
    def led_solid_color(self, color, duration=0):
        """Set all LEDs to one solid color"""
        for i in range(NUM_LEDS):
            np[i] = color
        np.write()
        if duration > 0:
            utime.sleep(duration)
    
    # ==================== SERVO MOVEMENT ====================
    def _smooth_move_servo(self, axis, target_degrees, duration=4.0):
        """Move servo smoothly"""
        start_ns = self.current_positions[axis]
        target_ns = self._degree_to_ns(target_degrees)
        
        if start_ns == target_ns:
            return True
        
        print(f"🔄 {axis.upper()}-axis: {self._ns_to_degree(start_ns)}° → {target_degrees}°")
        
        update_interval = 0.02
        total_updates = int(duration / update_interval)
        
        for i in range(total_updates + 1):
            t = i / total_updates
            ease_t = 0.5 - 0.5 * math.cos(t * math.pi)
            current_ns = int(start_ns + (target_ns - start_ns) * ease_t)
            self.servos[axis].duty_ns(current_ns)
            utime.sleep(update_interval)
        
        self.current_positions[axis] = target_ns
        return True
    
    def return_to_initial_with_leds(self):
        """Return to initial positions with LED sequence"""
        print("\n" + "="*50)
        print("🏠 RETURNING TO INITIAL POSITIONS")
        print("="*50)
        
        # 1. Quick brightness increase
        self.led_brightness_increase(duration=1.5)
        
        # 2. Rainbow effect
        self.led_rainbow_effect()
        
        # Now move servos to initial positions
        for axis, initial_deg in ServoConfig.INITIAL_POSITIONS.items():
            current_deg = self._ns_to_degree(self.current_positions[axis])
            if current_deg != initial_deg:
                print(f"Moving {axis.upper()}-axis to initial position...")
                self._smooth_move_servo(axis, initial_deg, duration=3.0)
                utime.sleep(0.3)
        
        print("✅ All servos at initial positions")
    
    def y_axis_sequence(self):
        """Y-axis movement with RED LEDs"""
        print("\n🎯 Y-AXIS SEQUENCE (RED LEDs)")
        self.led_solid_color((255, 0, 0))  # RED
        
        sequence = [90, 80, 120, 90]
        for target in sequence:
            self._smooth_move_servo('y', target, duration=3.0)
            utime.sleep(0.3)
        
        self.led_clear()
    
    def x_axis_sequence(self):
        """X-axis movement with GREEN LEDs"""
        print("\n🎯 X-AXIS SEQUENCE (GREEN LEDs)")
        self.led_solid_color((0, 255, 0))  # GREEN
        
        sequence = [80, 65, 110, 80]
        for target in sequence:
            self._smooth_move_servo('x', target, duration=3.0)
            utime.sleep(0.3)
        
        self.led_clear()
    
    def z_axis_sequence(self):
        """Z-axis movement with BLUE LEDs"""
        print("\n🎯 Z-AXIS SEQUENCE (BLUE LEDs)")
        self.led_solid_color((0, 0, 255))  # BLUE
        
        sequence = [90, 70, 120, 90]
        for target in sequence:
            self._smooth_move_servo('z', target, duration=3.0)
            utime.sleep(0.3)
        
        self.led_clear()
    
    def full_robot_sequence(self):
        """Complete robot sequence with LED effects"""
        print("\n" + "="*50)
        print("🤖 FULL ROBOT SEQUENCE STARTING")
        print("="*50)
        
        # Run sequences with colored LEDs
        self.y_axis_sequence()      # RED during movement
        utime.sleep(0.5)
        self.x_axis_sequence()      # GREEN during movement
        utime.sleep(0.5)
        self.z_axis_sequence()      # BLUE during movement
        
        # Final brightness decrease
        print("\n💡 Final brightness decrease...")
        self.led_brightness_decrease(duration=2.0)
        
        print("✅ Full sequence completed!")

# ==================== MAIN PROGRAM ====================
def main():
    robot = CompleteRobotController()
    
    print("\n" + "="*60)
    print("🌈 PIA-THE-ROBOT WITH LED SEQUENCE")
    print("="*60)
    print("Sequence:")
    print("1. Brightness increase (10→255)")
    print("2. Rainbow effect") 
    print("3. Return to initial positions")
    print("4. Y-axis movement 🔴 RED")
    print("5. X-axis movement 🟢 GREEN")  
    print("6. Z-axis movement 🔵 BLUE")
    print("7. Brightness decrease (255→10)")
    print("Press Ctrl+C to stop")
    print("="*60)
    
    utime.sleep(2)
    
    try:
        while True:
            # Start with LED sequence and return to initial
            robot.return_to_initial_with_leds()
            utime.sleep(1)
            
            # Run the main robot sequence
            robot.full_robot_sequence()
            utime.sleep(2)
            
            print("\n🔄 Restarting sequence in 3 seconds...")
            utime.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopping robot...")
        robot.led_clear()
        
    finally:
        print("\n🔌 Robot safely shut down")

# 🚀 RUN THE PROGRAM
if __name__ == "__main__":
    main()