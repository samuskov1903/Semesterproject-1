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
    connected = False
    while True:
        is_connected = (
            controller.connection is not None
            and controller.connection.is_connected()
        )
        if is_connected and not connected:
            print("Connected to car")
        connected = is_connected

      
    
        y_val = joystick_y.read()
        x_val = joystick_x.read()
             
        x_offset = (x_val - 32768) / 32768.0  # Skalerer værdien til mellem -1.0 og 1.0
        y_offset = (y_val - 32768) / 32768.0  # Skalerer værdien til mellem -1.0 og 1.0

        message = [x_offset, y_offset]
        try:
            controller.send(message)
        except RuntimeError as error:
            print(error)
        await asyncio.sleep_ms(50)


asyncio.run(main())