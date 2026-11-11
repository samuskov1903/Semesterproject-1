from time import sleep
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor


sensor_pin = 28
sensor_led_pin = 27
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
<<<<<<< HEAD

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.35)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.35)

motorleft.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
motorright.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
print(f"Skridt FØR bevægelse: {motorleft.total_steps}") 

robot = differentieldrive(motorleft, motorright, 8.6)
    
#robot.turn_on_wheel_robot_steps(1153, "left", 0.02)
motorleft.set_step_mode("full") # "full" for full step. "half" for half step og et nummer uden "" for micro
motorright.set_step_mode("full") # "full" for full step. "half" for half step og et nummer uden "" for micro

print(f"Skridt FØR bevægelse: {motorleft.total_steps}") 

robot.drive_robot_steps(600, "forward",0.02)
=======
wheel_diameter = 8.6
wheel_base = 24.5
log_file = "turns.txt"


ldr = Sensor(sensor_pin, sensor_led_pin)
ldr.light_led("on")

motorleft = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorright = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleft.set_step_mode("half")
motorright.set_step_mode("half")
>>>>>>> 95a73f19b579fa5ae8450e2c8d8d2ee6ec1ec812


robot = differentieldrive(
    motorleft,
    motorright,
    wheel_diameter,
    wheel_base,
)


try:
    with open(log_file, "w") as log:
        log.write("Sensor recordings\n")

    sleep(1)
    ldr.record_turn(robot, "left", log_file)

    sleep(1)
    ldr.record_turn(robot, "right", log_file)
finally:
    ldr.light_led("off")
    ldr.logging = False
    ldr.running = False
    robot.stop()
