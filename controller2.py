import asyncio
from connect import ControlBLE
from sensor import Sensor

# This Pico is the BLE server and joystick controller.
controller = ControlBLE()

# Read the vertical joystick axis from ADC pin 28.
joystick_y_pin = 26
joystick_y = Sensor(joystick_y_pin)

# Read the horizontal joystick axis from ADC pin 26.
joystick_x_pin = 28
joystick_x = Sensor(joystick_x_pin)

async def main():
    # Start the BLE advertising task in the background.
    asyncio.create_task(controller.advertise())
    connected = False
    disconnected = False
    while True:
        # Check whether the robot Pico is still connected.
        is_connected = (
            controller.connection is not None
            and controller.connection.is_connected()
        )

        # Print connection state changes only once.
        if is_connected and not connected:
            print("Connected to car")
            disconnected = False
        elif not is_connected and not disconnected:
            print("Waiting for connection to car...")
            disconnected = True
        connected = is_connected

        # Do not read or send joystick data while disconnected.
        if not is_connected:
            await asyncio.sleep_ms(500)
            continue

        # Read 16-bit ADC values (0 to 65535).
        y_val = joystick_y.read()
        x_val = joystick_x.read()
        print(x_val)

        # Convert the ADC values to joystick offsets from -1.0 to 1.0.
        x_offset = (x_val - 32768) / 32768.0  # Skalerer værdien til mellem -1.0 og 1.0
        y_offset = (y_val - 32768) / 32768.0  # Skalerer værdien til mellem -1.0 og 1.0

        # Send [horizontal, vertical] to the robot at 20 Hz.
        message = [x_offset, y_offset]
        try:
            controller.send(message)
        except RuntimeError as error:
            print(error)
        await asyncio.sleep_ms(50)


asyncio.run(main())