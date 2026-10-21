#Hussein Mohamed Kleit   hukle26@student.sdu.dk

from time import sleep
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
led_pins = [16, 17, 18, 19]

leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.35)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.35)

motorleft.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
motorright.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
print(f"Skridt FØR bevægelse: {motorleft.total_steps}") 

robot = differentieldrive(motorleft, motorright, 8.6)
    
#robot.turn_on_wheel_robot_steps(1153, "left", 0.02)

 #ændre værdierne til de ønskede værdier til bevægelsen

print(f"Skridt efter første bevægelse: {motorleft.total_steps}") #husk at ændre ordet "første" til "anden" til vis du laver en ny bevægelse

#hvis der skal være 2 bevægelser så kopier linje 14-16 og ændre værdiene til de ønskede værdier til næste bevægelse

robot.move_dist(100,"forward")