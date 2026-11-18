import asyncio
import aioble
import bluetooth



class ControlBLE:
    """Provide the robot's BLE service and receive messages from a controller."""

    def __init__(self):
        # Both endpoints must use the same custom 128-bit UUIDs.
        self.SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
        self.CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
        self.MESSAGE_INTERVAL = 0
        self.service = aioble.Service(self.SERVICE_UUID)
        # The characteristic supports reading, writing, and notifications.
        self.char = aioble.Characteristic(
            self.service, self.CHAR_UUID, read=True, write=True, notify=True, capture=True
        )
        # Make the service available to connected BLE clients.
        aioble.register_services(self.service)
    
    async def advertise(self):
        """Advertise the robot and process messages from connected clients."""
        while True:
            # Advertise until a client, such as pico_a, connects.
            print("Advertising...")
            connection = await aioble.advertise(
                250_000, name="pico-b", services=[self.SERVICE_UUID]
            )
            print("Connected to", connection.device)
            # Send a notification back to the connected client.
            self.char.notify(connection, b"pong")
            
            # Handle messages while the client remains connected.
            while connection.is_connected():
                try:
                    # Wait up to one second for the client to write data.
                    _, data = await self.char.written(timeout_ms=1000)
                    print("B received:", data)
                except asyncio.TimeoutError:
                    # No message arrived; keep waiting for the next one.
                    pass
                except aioble.DeviceDisconnectedError:
                    # Leave the inner loop and advertise again for another client.
                    break

class CarBle:
    """Connect to the robot's BLE service and exchange messages with it."""

    def __init__(self):
        self.SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
        self.CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
        self.MESSAGE_INTERVAL = 0
        self.connection = None
        self.char = None
        
            
    async def connect(self):
        """Scan for the robot and return its device when it is found."""
        # Scan for up to five seconds. Active scanning asks devices for extra
        # advertising data, including the advertised name and service UUID.
                async with aioble.scan(5000, interval_us=300, window_us=30000, active=True) as scanner:
                    async for result in scanner:
                        # Only accept the intended device, and verify that it offers the
                        # service this client needs.
                        if result.name() == "pico-b" and self.SERVICE_UUID in result.services():
                            return result.device
                # No matching device was found during this scan.
                return None 
            
    async def FindController(self):
        """Keep scanning until the robot is found, then return its BLE handles."""
        device = None
        while device is None:
            print("Scanning...")
            device = await self.connect()
    
        # Resolve the service and characteristic exposed by the robot.
        connection = await device.connect()
        service = await connection.service(self.SERVICE_UUID)
        char = await service.characteristic(self.CHAR_UUID)
        # Subscribe so listen() can receive notifications from the robot.
        await char.subscribe(notify=True)

        self.connection = connection
        self.char = char
        return connection, char

    async def send(self, message):
        """Send bytes to the connected Pico."""
        if self.char is None:
            raise RuntimeError("BLE is not connected")
        # Accept text as a convenience, but always send bytes over BLE.
        if isinstance(message, str):
            message = message.encode()
        await self.char.write(message)

    async def listen(self, handler):
        """Handle notifications without blocking the rest of the controller."""
        if self.char is None:
            raise RuntimeError("BLE is not connected")

        # Wait for notifications until the remote device disconnects.
        while self.connection.is_connected():
            try:
                data = await self.char.notified()
                await handler(data)
            except aioble.DeviceDisconnectedError:
                break


    