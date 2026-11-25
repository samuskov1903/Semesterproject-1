from time import sleep, sleep_ms
from sensor import Sensor
from Differential_drive import differentieldrive
from stepper_motor import StepperMotor
from Navigation import Navigation
from multiplexer_data import Multiplexer_data


sensor1_pin = 28
sensor1_led_pin = 27
sensor2_pin = 26
sensor2_led_pin = 22
leftmotor_pins = [0, 1, 2, 3]
rightmotor_pins = [4, 5, 6, 7]
wheel_diameter = 8.6
wheel_base = 24.5
log_file = "turns.txt"


ldrleft = Sensor(sensor1_pin, sensor1_led_pin)
ldrleft.light_led("on")
ldrright = Sensor(sensor2_pin, sensor2_led_pin)
ldrright.light_led("on")


motorleftfull = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorrightfull = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleftmicro = StepperMotor(leftmotor_pins, pwm_pct=0.2)
motorrightmicro = StepperMotor(rightmotor_pins, pwm_pct=0.2)
motorleftfull.set_step_mode("full")
motorrightfull.set_step_mode("full")
motorleftmicro.set_step_mode(4)
motorrightmicro.set_step_mode(4)



robotfull = differentieldrive(
    motorleftfull,
    motorrightfull,
    wheel_diameter,
    wheel_base
)
robotmicro = differentieldrive(
    motorleftmicro, 
    motorrightmicro, 
    wheel_diameter, 
    wheel_base)
rute = Navigation(14)




#for i in rute.rute3tilbage :
#    print(i)
#   robotfull.drive_to_junction(i, 0.005, robotmicro, ldrleft, ldrright)
    


#sleep(2)
#robotfull.turn_on_point_robot_angle(180, "left", 0.01)



sleep_ms(2000)

Bedre = Multiplexer_data()

sleep_ms(100)

while True:
    liste = Bedre.bin_scan_all_sensors()
    if liste[1] ==0 :
        robotmicro.turn_curve_cm(1, "left", 0.004, 5)
    elif liste[4] == 0:
        robotmicro.turn_curve_cm(1, "right",0.004, 5)
    elif liste[2] == 0:
        robotmicro.turn_curve_cm(1, "left", 0.002, 2)
    elif liste[3] == 0:
        robotmicro.turn_curve_cm(1, "right", 0.002, 2)
    robotmicro.move_dist(1, "forward", 0.002)











