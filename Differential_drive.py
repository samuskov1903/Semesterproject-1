from time import sleep
import math


# Coordinate the two stepper motors for driving and turning.
class differentieldrive :
    def __init__(self, left, right, wheel_dia, wheel_base):
        # Store the motors and the wheel measurements.
        self.motorleft = left
        self.motorright = right
        self.wheel_dia = wheel_dia
        self.wheel_base = wheel_base
        self.wheel_circumfrence = self.wheel_base * math.pi
        self.wheel_rev = self.wheel_circumfrence/(self.wheel_dia*math.pi)


    def stop(self):
        # Turn off both motors.
        self.motorleft.stop()
        self.motorright.stop()  
        
    def turn_on_wheel_robot_steps(self, steps, direction, delay) : # Turn around one wheel for a specified number of steps.
            # Move only the wheel on the outside of the turn.
            try:
                for _ in range(round(steps)):
                    if direction == "left":
                        self.motorright.step_once("forward")
                    elif direction == "right":
                        self.motorleft.step_once("forward")
                        
                    sleep(delay)
            finally :
                self.stop()  
                    
    def turn_on_wheel_robot_angle(self, angle, direction, delay):
        # Turn around one stationary wheel by moving the other wheel along an arc.
        # Convert the requested angle into motor steps.
        step_360_degree = self.wheel_rev * 50 * len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree * 2
        
        # Select the moving wheel based on the turn direction.
        self.turn_on_wheel_robot_steps(steps, direction, delay)   
        
    def turn_on_point_robot_steps(self, steps, direction, delay) : # Turn in place using both wheels.
            try:
                for _ in range(round(steps)):
                    if direction == "right":
                        self.motorright.step_once("forward")
                        self.motorleft.step_once("backward")            
                    elif direction == "left" :
                        self.motorright.step_once("backward")
                        self.motorleft.step_once("forward")
                    sleep(delay)
            finally :
                # Stop both wheels when the turn is complete or interrupted.
                self.stop()      

    def turn_on_point_robot_angle(self, angle, direction, delay=0.02): # Turn in place through an angle.
        # Convert the requested angle into motor steps.
        step_360_degree = self.wheel_rev*50*len(self.motorleft.sequence)
        steps = angle*(step_360_degree/360)     
        # Move both wheels in opposite directions.
        self.turn_on_point_robot_steps(steps, direction, delay)

  
    def drive_robot_steps(self, steps, direction="forward", delay=0.01) : # Drive both wheels for a number of steps.
        # Use each motor's step index to preserve its current phase.
        try:
            for _ in range(round(steps)):
                self.motorright.step_once(direction)
                self.motorleft.step_once(direction)
                sleep(delay)
        finally:
            self.stop()
            
    def cm_to_steps(self, dist_cm):
            # Convert a distance in centimeters into wheel rotations.
            self.dist_cm = dist_cm 
            revs_for_dist = self.dist_cm/(self.wheel_dia*math.pi) # Convert distance to wheel rotations.
            steps_for_dist = revs_for_dist * len(self.motorright.modes[self.motorright.current_mode])*50 # Convert wheel rotations to motor steps.
            return steps_for_dist # Return the required number of motor steps.

    def move_dist(self, distance_cm, direction, delay=0.01): # Move a distance in the requested direction.
        # Convert the distance into steps and drive both wheels.
        steps = round(self.cm_to_steps(distance_cm))
        self.drive_robot_steps(steps, direction, delay)
        self.stop()

    def turn_curve_cm(self, cm, direction, delay, ratio) :
        steps = self.cm_to_steps(cm)
        self.turn_curve(steps, direction, delay, ratio)

    
    def turn_curve(self, steps, direction, delay, ratio):
        try:
            for _ in range(round(steps)):
                if direction == "left" :
                    for _ in range(ratio):
                        self.motorright.step_once("forward")
                        sleep(delay/steps)
                    self.motorleft.step_once("forward")
                    sleep(delay)
                elif direction == "right" :
                    for _ in range(ratio):
                        self.motorleft.step_once("forward")
                        sleep(delay/steps)
                    self.motorright.step_once("forward")
                    sleep(delay)
                    
        finally:
            self.stop()