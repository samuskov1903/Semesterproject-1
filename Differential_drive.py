from time import sleep
import math


# Coordinate the two stepper motors to move and turn the robot.
class differentieldrive :
    def __init__(self, left, right, wheel_dia, wheel_base):
        # Store both motors and the diameter of the robot's wheels.
        self.motorleft = left
        self.motorright = right
        self.wheel_dia = wheel_dia
        self.wheel_base = wheel_base
        self.wheel_circmunfrence = self.wheel_base * math.pi
        self.wheel_rev = wheel_circmunfrence/(self.wheel_dia*math.pi)
        # Select the step sequence for each motor's current stepping mode.
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 

    def stop(self):
        # Turn off both motors.
        self.motorleft.stop()
        self.motorright.stop()  
        
    def turn_on_wheel_robot_steps(self, steps, direction, delay) : # Turn around one wheel for a specified number of steps.
            # Drive only the right wheel for a left turn.
            if direction == "left" :
                self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
                try:
                    for i in range(round(steps)):
                        if direction == "left":
                            self.motorright.step_once("forward")
                        elif direction == "right":
                            self.motorleft.step_once("forward")
                            
                        sleep(delay)
                finally :
                    self.stop()  
                    
    def turn_on_wheel_robot_angle(self, angle, direction, delay):
        # Turn around one wheel so the robot follows an arc.
        # Estimate the motor steps needed to turn through the requested angle.
        step_360_degree = self.wheel_rev * 50 * len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree * 2
        
        # A left turn is made by driving only the right wheel.
        self.turn_on_wheel_robot_steps(steps, direction, delay)   
        
    def turn_on_point_robot_steps(self, steps, direction, delay) : # Turn the robot in place for a specified number of steps.
            try:
                for i in range(round(steps)):
                    if direction == "right":
                        self.motorright.step_once("forward")
                        self.motorleft.step_once("backward")            
                    elif direction == "left" :
                        self.motorright.step_once("backward")
                        self.motorleft.step_once("forward")
                    sleep(delay)
            finally :
                # Stop both wheels when the requested turn is complete or interrupted.
                self.stop()      

    def turn_on_point_robot_angle(self, angle, direction, delay=0.02): # Turn the robot through an angle in place.
        # Calculate the steps needed for the wheels to turn the robot in place.
        step_360_degree = self.wheel_rev*50*len(self.motorleft.sequence)
        steps = angle*(step_360_degree/360)     
        # Reverse one wheel's sequence so the wheels turn in opposite directions.
        self.turn_on_point_robot_steps(steps, direction, delay)

  
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
        steps = round(self.cm_to_steps(distance_cm))
        self.drive_robot_steps(steps, direction, delay)
        self.stop()