from machine import Pin, PWM
import utime
import math

# ==================== MULTI-SERVO CONFIGURATION ====================
class MultiServoConfig:
    # Servo PWM values (nanoseconds)
    SERVO_RANGE = {
        'min': 1000000,    # 0 degrees
        'mid': 1500000,    # 90 degrees  
        'max': 2000000     # 180 degrees
    }
    
    # Servo pin assignments
    SERVO_PINS = {
        'y': 15,  # Y-axis servo
        'x': 14,  # X-axis servo  
        'z': 13   # Z-axis servo
    }
    
    # Initial positions (in degrees)
    INITIAL_POSITIONS = {
        'y': 90,  # Y starts at 90°
        'x': 80,  # X starts at 80°
        'z': 90   # Z starts at 90°
    }

# ==================== ADVANCED MULTI-SERVO CONTROLLER ====================
class AdvancedMultiServoController:
    def __init__(self):
        self.servos = {}
        self.current_positions = {}
        self.is_moving = False
        
        # Initialize all servos
        for axis, pin in MultiServoConfig.SERVO_PINS.items():
            self.servos[axis] = PWM(Pin(pin))
            self.servos[axis].freq(50)
            
            # Convert degree to nanoseconds and set initial position
            initial_deg = MultiServoConfig.INITIAL_POSITIONS[axis]
            initial_ns = self._degree_to_ns(initial_deg)
            self.current_positions[axis] = initial_ns
            self.servos[axis].duty_ns(initial_ns)
        
        utime.sleep(5)  # Let servos stabilize
        print("🤖 Multi-Servo Controller Initialized")
        self.print_status()
    
    def _degree_to_ns(self, degrees):
        """Convert degrees to PWM nanoseconds"""
        degrees = max(0, min(180, degrees))  # Clamp to valid range
        min_ns = MultiServoConfig.SERVO_RANGE['min']
        max_ns = MultiServoConfig.SERVO_RANGE['max']
        return int(min_ns + (degrees / 180) * (max_ns - min_ns))
    
    def _ns_to_degree(self, ns):
        """Convert PWM nanoseconds to degrees"""
        min_ns = MultiServoConfig.SERVO_RANGE['min']
        max_ns = MultiServoConfig.SERVO_RANGE['max']
        return int((ns - min_ns) / (max_ns - min_ns) * 180)
    
    def _smooth_move_servo(self, axis, target_degrees, duration=4.0):
        """
        Move a single servo smoothly from its current position to target
        """
        if axis not in self.servos:
            print(f"❌ Servo {axis} not found")
            return False
        
        start_ns = self.current_positions[axis]
        target_ns = self._degree_to_ns(target_degrees)
        
        if start_ns == target_ns:
            return True  # Already at target
        
        print(f"🔄 {axis.upper()}-axis: {self._ns_to_degree(start_ns)}° → {target_degrees}°")
        
        update_interval = 0.02  # 20ms updates
        total_updates = int(duration / update_interval)
        
        for i in range(total_updates + 1):
            t = i / total_updates
            # Smooth cosine easing
            ease_t = 0.5 - 0.5 * math.cos(t * math.pi)
            
            current_ns = int(start_ns + (target_ns - start_ns) * ease_t)
            self.servos[axis].duty_ns(current_ns)
            utime.sleep(update_interval)
        
        # Final position update
        self.current_positions[axis] = target_ns
        self.servos[axis].duty_ns(target_ns)
        return True
    
    def move_servo(self, axis, target_degrees, duration=4.0):
        """Move a single servo smoothly"""
        return self._smooth_move_servo(axis, target_degrees, duration)
    
    def move_servo_sequence(self, axis, sequence_degrees, durations=None):
        """
        Move a servo through a sequence of positions
        sequence_degrees: list of target degrees [pos1, pos2, pos3...]
        durations: optional list of durations for each movement
        """
        if not sequence_degrees:
            return False
        
        if durations is None:
            durations = [4.0] * len(sequence_degrees)
        
        print(f"🎬 {axis.upper()}-axis sequence: {sequence_degrees}")
        
        for i, target_deg in enumerate(sequence_degrees):
            duration = durations[i] if i < len(durations) else 4.0
            if not self._smooth_move_servo(axis, target_deg, duration):
                return False
            utime.sleep(0.5)  # Pause between sequence points
        
        return True
    
    def coordinated_move(self, movements, duration=4.0):
        """
        Move multiple servos simultaneously
        movements: dict like {'y': 90, 'x': 80, 'z': 90}
        """
        if self.is_moving:
            print("⚠️  Another movement in progress")
            return False
        
        self.is_moving = True
        print("🤝 Coordinated multi-servo movement")
        
        # Calculate starting positions and targets
        start_positions = {}
        target_positions = {}
        
        for axis, target_deg in movements.items():
            if axis in self.servos:
                start_positions[axis] = self.current_positions[axis]
                target_positions[axis] = self._degree_to_ns(target_deg)
        
        update_interval = 0.01
        total_updates = int(duration / update_interval)
        
        # Move all servos simultaneously
        for i in range(total_updates + 1):
            t = i / total_updates
            ease_t = 0.5 - 0.5 * math.cos(t * math.pi)
            
            for axis in movements.keys():
                if axis in self.servos:
                    start_ns = start_positions[axis]
                    target_ns = target_positions[axis]
                    current_ns = int(start_ns + (target_ns - start_ns) * ease_t)
                    self.servos[axis].duty_ns(current_ns)
            
            utime.sleep(update_interval)
        
        # Update final positions
        for axis, target_ns in target_positions.items():
            self.current_positions[axis] = target_ns
            self.servos[axis].duty_ns(target_ns)
        
        self.is_moving = False
        print("✅ Coordinated movement completed")
        return True
    
    def y_axis_sequence(self, duration=4.0):
        """Y-axis: 90° → 85° → 120° → 90°"""
        sequence = [90, 75, 130, 90]
        print("\n🎯 Y-AXIS SEQUENCE: 90° → 85° → 120° → 90°")
        return self.move_servo_sequence('y', sequence, [duration] * len(sequence))
    
    def z_axis_sequence(self, duration=4.0):
        """Z-axis: 90° → 85° → 120° → 90°"""  
        sequence = [90, 60, 130, 90]
        print("\n🎯 Z-AXIS SEQUENCE: 90° → 85° → 120° → 90°")
        return self.move_servo_sequence('z', sequence, [duration] * len(sequence))
    
    def x_axis_sequence(self, duration=4.0):
        """X-axis: 80° → 65° → 110° → 80°"""
        sequence = [80, 60, 130, 80]
        print("\n🎯 X-AXIS SEQUENCE: 80° → 65° → 110° → 80°")
        return self.move_servo_sequence('x', sequence, [duration] * len(sequence))
    
    def full_robot_sequence(self, duration=4.0):
        """
        Complete robot sequence:
        1. Y-axis movement
        2. X-axis movement  
        3. Z-axis movement
        """
        print("\n" + "="*50)
        print("🤖 FULL ROBOT SEQUENCE")
        print("="*50)
        
        # Y-axis first
        if not self.y_axis_sequence(duration):
            return False
        utime.sleep(0.5)
        
        # Then X-axis
        if not self.x_axis_sequence(duration):
            return False
        utime.sleep(0.5)
        
        # Then Z-axis
        if not self.z_axis_sequence(duration):
            return False
        
        print("✅ Full robot sequence completed")
        return True
    
    def safe_return_from_anywhere(self, duration=5.0):
        """
        Smoothly return all servos to initial positions from ANY current position
        This is the key feature you wanted - no jerks!
        """
        print("\n" + "="*50)
        print("🏠 SMOOTH RETURN FROM CURRENT POSITIONS")
        print("="*50)
        
        target_positions = {}
        for axis, initial_deg in MultiServoConfig.INITIAL_POSITIONS.items():
            current_deg = self._ns_to_degree(self.current_positions[axis])
            target_positions[axis] = initial_deg
            print(f"📊 {axis.upper()}-axis: {current_deg}° → {initial_deg}°")
        
        return self.coordinated_move(target_positions, duration)
    
    def get_current_angles(self):
        """Get current angles of all servos in degrees"""
        angles = {}
        for axis in self.servos.keys():
            angles[axis] = self._ns_to_degree(self.current_positions[axis])
        return angles
    
    def print_status(self):
        """Print current status of all servos"""
        print("\n" + "="*40)
        print("🤖 MULTI-SERVO STATUS")
        print("="*40)
        angles = self.get_current_angles()
        for axis, angle in angles.items():
            print(f"📍 {axis.upper()}-axis: {angle}°")
        print("="*40)

# ==================== MAIN APPLICATION ====================
def main():
    # Initialize multi-servo controller
    robot = AdvancedMultiServoController()
    
    print("\n" + "="*60)
    print("🤖 PIA-THE-ROBOT MULTI-SERVO CONTROLLER")
    print("="*60)
    print("Features:")
    print("• Individual servo control")
    print("• Predefined sequences for Y, X, Z axes") 
    print("• Coordinated multi-servo movements")
    print("• Smooth return from ANY position (no jerks!)")
    print("• Continuous operation with safe interrupt")
    print("="*60)
    
    try:
        # Run continuous sequences
        sequence_count = 0
        
        while True:
            sequence_count += 1
            print(f"\n🎬 ROBOT SEQUENCE #{sequence_count}")
            print("-" * 40)
            
            # Run full sequence
            robot.full_robot_sequence(duration=4.0)
            
            # Print status every few sequences
            if sequence_count % 3 == 0:
                robot.print_status()
            
            utime.sleep(2.0)  # Pause between full sequences
            
    except KeyboardInterrupt:
        print("\n\n⚠️  USER INTERRUPT DETECTED")
        robot.print_status()
        print("\n🔄 Smoothly returning to initial positions...")
        robot.safe_return_from_anywhere(duration=5.0)
        
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        print("🔄 Emergency return to initial positions...")
        robot.safe_return_from_anywhere(duration=5.0)
        
    finally:
        print("\n" + "="*60)
        print("🏁 PROGRAM COMPLETED")
        robot.print_status()
        print("🔌 Safe to power off")
        print("="*60)

# ==================== QUICK TEST FUNCTIONS ====================
def test_individual_servos():
    """Test each servo individually"""
    robot = AdvancedMultiServoController()
    
    print("🧪 TESTING INDIVIDUAL SERVOS")
    
    # Test Y-axis
    print("\n🎯 Testing Y-axis...")
    robot.y_axis_sequence(duration=3.0)
    utime.sleep(0.5)
    
    # Test X-axis  
    print("\n🎯 Testing X-axis...")
    robot.x_axis_sequence(duration=3.0)
    utime.sleep(0.5)
    
    # Test Z-axis
    print("\n🎯 Testing Z-axis...")
    robot.z_axis_sequence(duration=3.0)
    utime.sleep(0.5)
    
    # Return to initial positions
    robot.safe_return_from_anywhere()

def test_emergency_return():
    """Test the emergency return feature from random positions"""
    robot = AdvancedMultiServoController()
    
    print("🚨 TESTING EMERGENCY RETURN FROM RANDOM POSITIONS")
    
    # Move servos to random positions
    robot.move_servo('y', 45, duration=2.0)
    robot.move_servo('x', 110, duration=2.0) 
    robot.move_servo('z', 135, duration=2.0)
    
    robot.print_status()
    utime.sleep(0.5)
    
    # Now smoothly return to initial positions
    robot.safe_return_from_anywhere(duration=4.0)
    robot.print_status()

# 🚀 EXECUTION POINT
if __name__ == "__main__":
    # Run the main multi-servo sequence
    main()
    
    # Uncomment to test individual servos:
    # test_individual_servos()
    
    # Uncomment to test emergency return:
    # test_emergency_return()