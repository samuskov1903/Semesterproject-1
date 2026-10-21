from stepper_motor import StepperMotor

motor = StepperMotor([1,2,3,4])
print(motor.generate_microstep_sequence(2))