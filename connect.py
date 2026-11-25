import asyncio
import aioble
import bluetooth



class ControlBLE:
    """Provide the robot's BLE service and receive messages from a controller."""

    def __init__(self):
        # Both Picos must use matching service and characteristic UUIDs.
        self.SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
        self.CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

        # Create the BLE service and notification characteristic.
        self.service = aioble.Service(self.SERVICE_UUID)
        self.char = aioble.Characteristic(
            self.service, self.CHAR_UUID, read=True, write=True, notify=True, capture=True
        )
        self.connection = None

        # Make the service available to connected BLE clients.
        aioble.register_services(self.service)
    
    async def advertise(self):
        """Advertise the robot and process messages from connected clients."""
        while True:
            # Advertise this device for discovery by the car Pico.
            print("Advertising...")
            self.connection = None
            try:
                connection = await aioble.advertise(
                    250_000, name="pico-b", services=[self.SERVICE_UUID]
                )
                print("Connected to", connection.device)
                self.connection = connection

                # Send an initial notification after connecting.
                self.char.notify(connection, b"pong")

                # Keep the connection active until the client disconnects.
                while connection.is_connected():
                    try:
                        # Wait for a BLE write from the robot Pico.
                        _, data = await self.char.written(timeout_ms=1000)
                        print("B received:", data)
                    except asyncio.TimeoutError:
                        # A timeout is normal and does not mean the BLE link is lost.
                        pass
                    except aioble.DeviceDisconnectedError:
                        break
            except aioble.DeviceDisconnectedError:
                pass
            finally:
                self.connection = None

    def send(self, message):
        """Send bytes to the connected Pico."""
        # Refuse to send if there is no live BLE connection.
        if self.connection is None or not self.connection.is_connected():
            raise RuntimeError("BLE is not connected")

        # Convert supported message types into bytes for notification.
        if isinstance(message, str):
            message = message.encode()
        elif isinstance(message, list):
            message = repr(message).encode()
        print("Sending:", message)
        try:
            self.char.notify(self.connection, message)
        except aioble.DeviceDisconnectedError:
            self.connection = None
            raise RuntimeError("BLE is not connected")

class CarBle:
    """Connect to the robot's BLE service and exchange messages with it."""

    def __init__(self):
        # These UUIDs must match ControlBLE on the controller Pico.
        self.SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
        self.CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
        self.connection = None
        self.char = None
        
            
    async def connect(self):
        """Scan for the robot and return its device when it is found."""
        # Scan for up to five seconds. Active scanning asks devices for extra
        # advertising data, including the advertised name and service UUID.
        async with aioble.scan(
            5000, interval_us=30000, window_us=15000, active=True
        ) as scanner:
            async for result in scanner:
                name = result.name()
                if name:
                    print("Found BLE device:", name)

                # Some aioble builds do not include both fields in every
                # scan response, so accept either identifier.
                if name == "pico-b" or self.SERVICE_UUID in result.services():
                    return result.device
            return None 
            
    async def FindController(self):
        """Keep scanning until the robot is found, then return its BLE handles."""
        device = None
        while device is None:
            print("Scanning...")
            device = await self.connect()
            if device is None:
                # Avoid starting a new scan immediately when none is found.
                await asyncio.sleep(1)

        # Connect and resolve the matching service and characteristic.
        connection = await device.connect()
        try:
            service = await connection.service(self.SERVICE_UUID)
            char = await service.characteristic(self.CHAR_UUID)
        except BaseException:
            if connection.is_connected():
                await connection.disconnect()
            raise

        # Subscribe so listen() can receive notifications from the robot.
        await char.subscribe(notify=True)

        self.connection = connection
        self.char = char
        return connection, char


    async def listen(self, handler):
        """Handle notifications without blocking the rest of the controller."""
        if self.char is None:
            raise RuntimeError("BLE is not connected")

        # Pass each notification to the handler until the link drops.
        try:
            while self.connection.is_connected():
                try:
                    data = await self.char.notified()
                    await handler(data)
                except aioble.DeviceDisconnectedError:
                    break
        finally:
            self.connection = None
            self.char = None


    