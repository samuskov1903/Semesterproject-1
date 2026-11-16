import asyncio

import aioble
import bluetooth


SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")


class ControlBLE:
    """Expose the robot's BLE service and receive controller messages."""

    def __init__(self):
        self.SERVICE_UUID = SERVICE_UUID
        self.CHAR_UUID = CHAR_UUID
        self.MESSAGE_INTERVAL = 0
        self.service = aioble.Service(self.SERVICE_UUID)
        self.char = aioble.Characteristic(
            self.service,
            self.CHAR_UUID,
            read=True,
            write=True,
            notify=True,
            capture=True,
        )
        aioble.register_services(self.service)

    async def advertise(self):
        """Advertise until a client connects, then handle its messages."""
        while True:
            print("Advertising...")
            connection = await aioble.advertise(
                250_000,
                name="pico-b",
                services=[self.SERVICE_UUID],
            )
            print("Connected to", connection.device)
            self.char.notify(connection, b"pong")

            while connection.is_connected():
                try:
                    _, data = await self.char.written(timeout_ms=1000)
                    print("B received:", data)
                except asyncio.TimeoutError:
                    continue
                except aioble.DeviceDisconnectedError:
                    break


class CarBle:
    """Connect to the robot's BLE service as a controller."""

    def __init__(self):
        self.SERVICE_UUID = SERVICE_UUID
        self.CHAR_UUID = CHAR_UUID
        self.MESSAGE_INTERVAL = 0

    async def connect(self):
        """Find the advertised robot and return its device, if present."""
        async with aioble.scan(
            5000,
            interval_us=300,
            window_us=30000,
            active=True,
        ) as scanner:
            async for result in scanner:
                if (
                    result.name() == "pico-b"
                    and self.SERVICE_UUID in result.services()
                ):
                    return result.device
        return None

    async def FindController(self):
        """Scan until the robot is found and return its connection and characteristic."""
        device = None
        while device is None:
            print("Scanning...")
            device = await self.connect()

        connection = await device.connect()
        service = await connection.service(self.SERVICE_UUID)
        char = await service.characteristic(self.CHAR_UUID)
        await char.subscribe(notify=True)
        return connection, char