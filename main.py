#Hussein Mohamed Kleit   hukle26@student.sdu.dk

from time import sleep
from stepper_motor import StepperMotor

led_pins = [16, 17, 18, 19]

motor1_pins = [0, 1, 2, 3]
motor2_pins = [4, 5, 6, 7]

motor1 = StepperMotor(motor1_pins, pwm_pct=0.35)
motor2 = StepperMotor(motor2_pins, pwm_pct=0.35)

motor1.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
motor2.set_step_mode("half") # "full" for full step. "half" for half step og et nummer uden "" for micro
print(f"Skridt FØR bevægelse: {motor1.total_steps}") 


def move_robot(steps, direction="forward", delay=0.01):
    i = 0
    n = 0
    motor1.sequence = motor1.modes[motor1.current_mode]
    motor2.sequence = motor2.modes[motor2.current_mode]
    if direction == "backward":
        motor1.sequence = list(reversed(motor1.sequence))
        motor2.sequence = list(reversed(motor2.sequence))
    try:
        for i in range(steps):
            motor1.set_step(motor1.sequence[n])
            motor2.set_step(motor2.sequence[n])
            if n >= len(motor1.sequence) - 1:
                n = 0
            else:
                n = n+1
            sleep(delay)
    finally :
        motor1.stop()
        motor2.stop()

move_robot(200, direction="forward", delay=0.01) #ændre værdierne til de ønskede værdier til bevægelsen

print(f"Skridt efter første bevægelse: {motor1.total_steps}") #husk at ændre ordet "første" til "anden" til vis du laver en ny bevægelse

#hvis der skal være 2 bevægelser så kopier linje 14-16 og ændre værdiene til de ønskede værdier til næste bevægelse