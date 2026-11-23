from connect import CarBle
from stepper_motor import StepperMotor
from Differential_drive import differentieldrive
import asyncio
from time import sleep
from OldController import Controller

leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5

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


async def handle_message(message):
    try:
        text = message.decode()
        text = text.strip().strip("[]")
        parts = text.split(",")
        turn = float(parts[0])
        speed = float(parts[1])
    except (UnicodeError, ValueError, IndexError, AttributeError):
        return

    print("Controller values:", turn, speed)

    try:
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


async def main():
    car = CarBle()
    while True:
        try:
            print("Searching for controller Pico...")
            await car.FindController()
            print("Connected to controller Pico")
            await car.listen(handle_message)
        except Exception as error:
            print("BLE error:", error)
        await asyncio.sleep(1)


asyncio.run(main())