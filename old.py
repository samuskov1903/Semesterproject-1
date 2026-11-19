delays = [0.25, 0.166, 0.111, 0.074, 0.049, 0.033, 0.022, 0.014, 0.001]

def speed_control(raw_val):
    raw_val = max(0, min(65535, raw_val))  
    zone_størrelse = 65535 / 19
    zone_indeks = int(raw_val / zone_størrelse)
    if zone_indeks > 18:
        zone_indeks = 18

    trin = zone_indeks - 9

    if trin == 0:
        return "stop", 0
    elif trin > 0:
        indeks = trin - 1
        return "forward", delays[indeks]
    else:
        indeks = abs(trin) - 1
        return "backwards", delays[indeks]


try:
    while True:
        raw_val = potentiometer.read()
        retning, nyt_delay = speed_control(raw_val)
        if retning == "stop":
            robot.stop()

        elif retning == "forward":
            motorleft.delay = nyt_delay
            motorright.delay = nyt_delay

        elif retning == "backwards":
            motorleft.delay = nyt_delay
            motorright.delay = nyt_delay

        sleep(0.05)
except KeyboardInterrupt:
    robot.stop()