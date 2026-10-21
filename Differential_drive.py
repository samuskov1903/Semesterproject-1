from time import sleep
from math import pi
class differentieldrive :
    def __init__(self, left, right, wheel_dia):
        self.motorleft = left
        self.motorright = right
        self.wheel_dia = wheel_dia
    def stop(self):
        self.motorleft.stop()
        self.motorright.stop()
    def turn_on_wheel_robot_steps(self, steps, direction, delay) :
        i = 0
        n = 0
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode]
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
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode]
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
        self.motorleft.sequence = self.motorleft.modes[self.motorleft.current_mode]
        self.motorright.sequence = self.motorright.modes[self.motorright.current_mode]
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
            steps_for_dist = revs_for_dist * len(self.motorright.sequence)*50
            
            return steps_for_dist

    def move_dist(self, distance_cm, direction, delay=0.01):
        steps = self.cm_to_steps(distance_cm)
        self.drive_robot_steps(steps, direction, delay)
        self.stop()