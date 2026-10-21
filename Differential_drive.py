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
    def turn_on_wheel_robot_angle(self, angle, direction, delay, wheel_dia = 8.5, wheel_base= 24.5 ):
        n = 0
        wheel_circmunfrence = wheel_base * math.pi
        wheel_rev = wheel_circmunfrence/(wheel_dia * math.pi)
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
    def turn_on_point_robot_angle(self, angle, direction, delay, wheel_dia = 8.5, wheel_base= 24.5):
        n = 0
        wheel_circmunfrence = wheel_base * math.pi
        print(wheel_circmunfrence)
        wheel_rev = wheel_circmunfrence/(wheel_dia*math.pi)
        print(wheel_rev)
        step_360_degree = wheel_rev*50*len(self.motorleft.sequence)
        print(step_360_degree)
        step_1_degree = step_360_degree/360
        print(step_1_degree)
        steps = angle*step_1_degree   
        print(steps)  
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
    def turn_on_wheel_robot_steps(self, steps, direction, delay) :
        i = 0
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
    def turn_on_point_robot_steps(self, steps, direction, delay) :
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

    def drive_robot_steps(self, steps, direction="forward", delay=0.01) :
        i = 0
        n = 0
        if direction == "backward":
            self.motorleft.sequence = list(reversed(self.motorleft.sequence))
            self.motorright.sequence = list(reversed(self.motorright.sequence))
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
            
    def cm_to_steps(self, dist_cm):
            self.dist_cm = dist_cm
            
            revs_for_dist = self.dist_cm/(self.wheel_dia*pi)
            steps_for_dist = revs_for_dist * len(self.motorright.modes[self.motorright.current_mode])*50
            print(self.motorright.current_mode)
            print(steps_for_dist)
            print(len(self.motorright.modes[self.motorright.current_mode]))
            return steps_for_dist

    def move_dist(self, distance_cm, direction, delay=0.01):
        steps = self.cm_to_steps(distance_cm)
        self.drive_robot_steps(steps, direction, delay)
        self.stop()