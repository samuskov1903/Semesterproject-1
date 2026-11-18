import asyncio
from connect import ControlBLE
from sensor import Sensor


controller = ControlBLE()

joystick_y_pin = 28
joystick_y = Sensor(joystick_y_pin)
joystick_x_pin = 26
joystick_x = Sensor(joystick_x_pin)

async def main():
    asyncio.create_task(controller.advertise())
    while True:
        message = [joystick_x.read(), joystick_y.read()]
        try:
            controller.send(message)
        except RuntimeError:
            pass
        await asyncio.sleep_ms(50)


asyncio.run(main())