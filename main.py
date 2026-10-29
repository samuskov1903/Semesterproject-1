#Hussein Mohamed Kleit   hukle26@student.sdu.dk

'''from time import sleep
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive

# GPIO pins assigned to the LEDs and the left and right stepper motors.
led_pins = [16, 17, 18, 19]
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

# Create the two motors with their four control pins and PWM power level.
motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)

# Use half-stepping for smoother movement; "full" selects other mode.
motorleft.set_step_mode("half")
motorright.set_step_mode("half")

# Create the differential drive using both motors and the wheel diameter.
robot = differentieldrive(motorleft, motorright, 8.6)

# Allow the hardware a moment to initialize before moving.
#sleep(2)
# Drive a square: move forward 100cm, then turn 90 degrees left, four times.
#robot.move_dist(5,"forward", 0.002)
for i in range(4):
    robot.move_dist(100,"forward", 0.002)
    sleep(1)
    robot.turn_on_point_robot_angle(90, "left", 0.01)
    sleep(1)'''
    

from sensor import Sensor
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import _thread
from time import sleep


sensor_pin = 28
led_pins = [16, 17, 18, 19]
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]

# Create the sensor
ldr = Sensor(sensor_pin)
# Create the two motors with their four control pins and PWM power level.
motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)

# Use half-stepping for smoother movement; "full" selects other mode.
motorleft.set_step_mode("half")
motorright.set_step_mode("half")

# Create the differential drive using both motors and the wheel diameter.
robot = differentieldrive(motorleft, motorright, 8.6)


    

# Starting thread with sensor
#_thread.start_new_thread(ldr.read_cont_bin_led(10, 40000, 5000), ())
_thread.start_new_thread(ldr.read_cont, (10,))

    
sleep(1)
robot.turn_on_point_robot_angle(180, "left", 0.01)
sleep(1)
robot.turn_on_point_robot_angle(180, "right", 0.01)
ldr.running = False
