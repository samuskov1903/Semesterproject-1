from time import sleep
import math


# Coordinate the two stepper motors to move and turn the robot.
class differentieldrive :
    def __init__(self, left, right, wheel_dia):
        # Store both motors and the diameter of the robot's wheels.
        self.motorleft = left
        self.motorright = right
        self.wheel_dia = wheel_dia
        # Select the step sequence for each motor's current stepping mode.
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 

    def stop(self):
        # Turn off both motors.
        self.motorleft.stop()
        self.motorright.stop()    

    def turn_on_wheel_robot_angle(self, angle, direction, delay, wheel_base= 24.5 ):
        # Turn around one wheel so the robot follows an arc.
        # Refresh the sequences in case a motor's stepping mode has changed.
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        n = 0
        # Estimate the motor steps needed to turn through the requested angle.
        wheel_circmunfrence = wheel_base * math.pi
        wheel_rev = wheel_circmunfrence/(self.wheel_dia * math.pi)
        step_360_degree = wheel_rev * 50 * len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree * 2
        n = 0
        if direction == "left" :
            # A left turn is made by driving only the right wheel.
            self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
            try:
                for i in range(steps):
                    # Apply the next right-motor state, wrapping at the end of its sequence.
                    self.motorright.set_step(self.motorright.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                            n = n+1
                    sleep(delay)
            finally :
                # Always release the motors, even if the loop is interrupted.
                self.stop()        
        elif direction == "right" :
            # A right turn is made by driving only the left wheel.
            self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
            try:
                for i in range(steps):
                    # Apply the next left-motor state, wrapping at the end of its sequence.
                    self.motorleft.set_step(self.motorleft.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                            n = n+1
                    sleep(delay)
            finally :
                self.stop()         

    def turn_on_point_robot_angle(self, angle, direction, delay=0.02, wheel_base= 25): # Turn the robot through an angle in place.
        # Reset the sequence index and use the current stepping mode.
        n = 0
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        # Calculate the steps needed for the wheels to turn the robot in place.
        wheel_circmunfrence = wheel_base * math.pi
        wheel_rev = wheel_circmunfrence/(self.wheel_dia*math.pi)
        step_360_degree = wheel_rev*50*len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree     
        # Reverse one wheel's sequence so the wheels turn in opposite directions.
        if direction == "right" :
            self.motorright.sequence = list(reversed(self.motorright.sequence))            
        elif direction == "left" :
            self.motorleft.sequence = list(reversed(self.motorleft.sequence)) 
        try:
            for i in range(steps):
                # Step both wheels together and wrap around their sequences as needed.
                self.motorleft.set_step(self.motorleft.sequence[n])
                self.motorright.set_step(self.motorright.sequence[n])
                if n >= len(self.motorleft.sequence) - 1:
                    n = 0
                else:
                    n = n+1
                sleep(delay)
        finally :
            # Stop both wheels when the requested turn is complete or interrupted.
            self.stop()   

    def turn_on_wheel_robot_steps(self, steps, direction, delay) : # Turn around one wheel for a specified number of steps.
        i = 0
        n = 0
        # Load the step sequences selected for each motor.
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        # Drive only the right wheel for a left turn.
        if direction == "left" :
            self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
            try:
                for i in range(steps):
                    # Move only the right wheel for a left turn.
                    self.motorright.set_step(self.motorright.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                        n = n+1
                    sleep(delay)
            finally :
                self.stop()        
        elif direction == "right" :
            self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
            try:
                for i in range(steps):
                    # Move only the left wheel for a right turn.
                    self.motorleft.set_step(self.motorleft.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                        n = n+1
                    sleep(delay)
            finally :
                self.stop()

    def turn_on_point_robot_steps(self, steps, direction, delay) : # Turn the robot in place for a specified number of steps.
        
        i = 0
        n = 0
        if direction == "right" :
            self.motorright.sequence = list(reversed(self.motorright.sequence))            
        elif direction == "left" :
            self.motorleft.sequence = list(reversed(self.motorleft.sequence)) 
        try:
            for i in range(steps):
                self.motorleft.set_step(self.motorleft.sequence[n])
                self.motorright.set_step(self.motorright.sequence[n])
                if n >= len(self.motorleft.sequence) - 1:
                    n = 0
                else:
                    n = n+1
                sleep(delay)
        finally :
            self.stop()
            
    def drive_robot_steps(self, steps, direction="forward", delay=0.01) : # Drive both motors for a specified number of steps.
        # Load the step sequences selected for the two motors.
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        i = 0
        n = 0
        if direction == "backward":
            # Reverse both sequences to drive backward.
            self.motorleft.sequence = list(reversed(self.motorleft.sequence))
            self.motorright.sequence = list(reversed(self.motorright.sequence))
        try:
            for i in range(steps):
                # Apply the same step in each sequence to drive both wheels.
                self.motorleft.set_step(self.motorleft.sequence[n])
                self.motorright.set_step(self.motorright.sequence[n])
                if n >= len(self.motorleft.sequence) - 1:
                    n = 0
                else:
                    n = n+1
                sleep(delay)
        finally :
            self.stop()
            
    def cm_to_steps(self, dist_cm):
            # Convert the requested distance from centimeters to wheel rotations.
            self.dist_cm = dist_cm 
            
            revs_for_dist = self.dist_cm/(self.wheel_dia*math.pi) # Convert distance to wheel rotations.
            steps_for_dist = revs_for_dist * len(self.motorright.modes[self.motorright.current_mode])*50 # Convert wheel rotations to motor steps.
            return steps_for_dist # Return the required motor steps.

    def move_dist(self, distance_cm, direction, delay=0.01): # Move a specified distance in the requested direction.
        # Convert the distance to motor steps, then drive both wheels.
        steps = self.cm_to_steps(distance_cm)
        self.drive_robot_steps(steps, direction, delay)
        self.stop()