from time import sleep
import math

class differentieldrive :
    def __init__(self, left, right, wheel_dia):
        self.motorleft = left
        self.motorright = right
        self.wheel_dia = wheel_dia
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
    def stop(self):
        self.motorleft.stop()
        self.motorright.stop()    
    def turn_on_wheel_robot_angle(self, angle, direction, delay, wheel_base= 24.5 ):
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        n = 0
        wheel_circmunfrence = wheel_base * math.pi
        wheel_rev = wheel_circmunfrence/(self.wheel_dia * math.pi)
        step_360_degree = wheel_rev * 50 * len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree * 2
        n = 0
        if direction == "left" :
            self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
            try:
                for i in range(steps):
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
                    self.motorleft.set_step(self.motorleft.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                            n = n+1
                    sleep(delay)
            finally :
                self.stop()         
    def turn_on_point_robot_angle(self, angle, direction, delay=0.02, wheel_base= 25): # turn a given angle around it self
        n = 0
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        wheel_circmunfrence = wheel_base * math.pi
        wheel_rev = wheel_circmunfrence/(self.wheel_dia*math.pi)
        step_360_degree = wheel_rev*50*len(self.motorleft.sequence)
        step_1_degree = step_360_degree/360
        steps = angle*step_1_degree     
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
    def turn_on_wheel_robot_steps(self, steps, direction, delay) : #makes the robot turn around the wheel a given amount of steps
        i = 0
        n = 0
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode] # sets the seqyence for the wheels
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        # tells the correct wheel to drive and the other to stand still
        if direction == "left" :  # tells the right wheel to turn
            self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
            try:
                for i in range(steps):
                    self.motorright.set_step(self.motorright.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                        n = n+1
                    sleep(delay)
            finally :
                self.stop()        
        elif direction == "right" : # makes the left wheel turn
            self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
            try:
                for i in range(steps):
                    self.motorleft.set_step(self.motorleft.sequence[n])
                    if n >= len(self.motorleft.sequence) - 1:
                        n = 0
                    else:
                        n = n+1
                    sleep(delay)
            finally :
                self.stop()
    def turn_on_point_robot_steps(self, steps, direction, delay) : # funtion that tells how many steps we rotate in a given direction
        
        i = 0
        n = 0
        if direction == "right" : # tells which wheel to turn backwards to make 
            self.motorright.sequence = list(reversed(self.motorright.sequence))            
        elif direction == "left" :
            self.motorleft.sequence = list(reversed(self.motorleft.sequence)) 
        self.drive_robot_steps(steps,direction,delay) #uses drive_robot_steps
    
    def drive_robot_steps(self, steps, direction="forward", delay=0.01) : # function to drive an amount of steps an amount of steps
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode] # defines the two sequences used
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode] 
        i = 0 # defines used variables
        n = 0
        if direction == "backward": # drives the sequence in reverse so it drives backwards
            self.motorleft.sequence = list(reversed(self.motorleft.sequence))
            self.motorright.sequence = list(reversed(self.motorright.sequence))
        try: # in try to make sure that it is stopped if anything happens
            for i in range(steps):# takes the amount of steps defined
                self.motorleft.set_step(self.motorleft.sequence[n])
                self.motorright.set_step(self.motorright.sequence[n])
                if n >= len(self.motorleft.sequence) - 1: # makes it loop
                    n = 0
                else:
                    n = n+1
                sleep(delay)
        finally :
            self.stop()
            
    def cm_to_steps(self, dist_cm):
            self.dist_cm = dist_cm 
            
            revs_for_dist = self.dist_cm/(self.wheel_dia*math.pi) # defines how many revs to turn for the given distance
            steps_for_dist = revs_for_dist * len(self.motorright.modes[self.motorright.current_mode])*50 # takes the revs and converts to steps
            return steps_for_dist # returns the amount of steps to take too drive the distance

    def move_dist(self, distance_cm, direction, delay=0.01): # function to move a set distance
        steps = self.cm_to_steps(distance_cm) # takes the steps from cm_to_step for the set distance and sets it to step
        self.drive_robot_steps(steps, direction, delay) #calls the drive funtion
        self.stop()