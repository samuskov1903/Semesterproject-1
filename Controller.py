import asyncio

from Connect import ControlBLE


async def run_controller_code(controller):
    """Run the robot code while BLE advertising remains active."""
    while True:
        # Replace this with the controller's normal robot code.
        print("Robot code is running")
        await asyncio.sleep(1)


async def main():
    controller = ControlBLE()
    ble_task = asyncio.create_task(controller.advertise())

    try:
        await run_controller_code(controller)
    finally:
        ble_task.cancel()
        try:
            await ble_task
        except asyncio.CancelledError:
            pass


asyncio.run(main())
