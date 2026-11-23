


from machine import Pin


# Configure every GPIO pin as an output and drive it low.
# This turns off LEDs, motor-driver inputs, and other GPIO loads.
for gpio_number in range(29):
    pin = Pin(gpio_number, Pin.OUT)
    pin.value(0)

# Turn off the Pico W's onboard LED.
try:
    led = Pin("LED", Pin.OUT)
    led.value(0)
except Exception:
    pass

print("All GPIO pins set low")
