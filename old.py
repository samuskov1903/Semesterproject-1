from time import sleep
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor
from OldController import Controller


leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5



potentiometer_pin = 27
potentiometer = Sensor(potentiometer_pin)
joystick_x_pin = 28
joystick_x = Sensor(joystick_x_pin)




motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("half")
motorright.set_step_mode("half")


robot = differentieldrive(
    motorleft,
    motorright,
    wheel_diameter,
    wheel_base,
)


try:
    while True:
        retning, nyt_delay, trin = Controller.speed_control(speed) 

       
        
    

        faktor = 0.02  # Bestemmer hvor voldsomt robotten drejer
        
    
        if retning == "stop":
            robot.stop()
            
        elif retning == "forward":
            motorleft.delay = max(0.001, nyt_delay + (turn * faktor))
            motorright.delay = max(0.001, nyt_delay - (turn * faktor))
            
        elif retning == "backwards":
            motorleft.delay = max(0.001, nyt_delay + (turn * faktor))
            motorright.delay = max(0.001, nyt_delay - (turn * faktor))
            
        sleep(0.05)

except KeyboardInterrupt:
    robot.stop()