import asyncio

from Connect import CarBle


async def handle_message(data):
    print("Message from robot:", data)


async def run_car_code(car):
    """Run the controller code while BLE remains active."""
    while True:
        # Replace this with the controller's normal code.
        await car.send("controller is running")
        await asyncio.sleep(1)


async def main():
    car = CarBle()
    await car.FindController()
    print("Connected to robot")

    ble_task = asyncio.create_task(car.listen(handle_message))
    try:
        await run_car_code(car)
    finally:
        ble_task.cancel()
        try:
            await ble_task
        except asyncio.CancelledError:
            pass


asyncio.run(main())
