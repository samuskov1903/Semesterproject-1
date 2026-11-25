from multiplexer_data import Multiplexer_data
from time import sleep_ms

sleep_ms(1000)

Bedre=Multiplexer_data()

sleep_ms(200)

while True:
    Bedre.bin_scan_all_sensors()
    sleep_ms(1)