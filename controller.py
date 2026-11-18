from time import sleep
import math

delays = [0.25, 0.166, 0.111, 0.074, 0.049, 0.033, 0.022, 0.014, 0.001]

class Controller:
    def speed_control(y_val):
        y_val = max(0, min(65535, y_val))
        zone_størrelse = 65535 / 19
        zone_indeks = int(y_val / zone_størrelse)
        if zone_indeks > 18:
            zone_indeks = 18

        trin = zone_indeks - 9

        if trin == 0:
            return "stop", 0, trin
        elif trin > 0:
            indeks = trin - 1
            return "forward", delays[indeks], trin
        else:
            indeks = abs(trin) - 1
            return "backwards", delays[indeks], trin





