#Hussein Mohamed Kleit   hukle26@student.sdu.dk

from machine import Pin, PWM
from time import sleep
import math
class StepperMotor:
    def __init__(self, pins, pwm_pct=0.15, frequency=18_000):
# Configure the four PWM outputs.
# Store each step sequence under a separate mode name.
# Keep track of the currently selected mode.
        self.outputs = [PWM(Pin(p, Pin.OUT)) for p in pins]
        for output in self.outputs:
            output.freq(frequency)
        val = pwm_pct
        self.modes = {
            "full": [
                [val, val, 0, 0],
                [0, val, val, 0],
                [0, 0, val, val],
                [val, 0, 0, val]
            ],
            "half": [
                [val, 0, 0, 0],
                [val, val, 0, 0],
                [0, val, 0, 0],
                [0, val, val, 0],
                [0, 0, val, 0],
                [0, 0, val, val],
                [0, 0, 0, val],
                [val, 0, 0, val]
            ]
        }
        self.current_mode = "full"
        self.total_steps = 0
    def set_step_mode(self, mode):
        # 1. Hvis man sender et tal (f.eks. motor.set_step_mode(4))
        if isinstance(mode, int):
            seq_name = f"micro_{mode}"
            self.modes[seq_name] = self.generate_microstep_sequence(mode)
            self.current_mode = seq_name
            self.step_index = 0
            
        # 2. Hvis man vælger 'full' eller 'half'
        elif mode in self.modes:
            self.current_mode = mode
            self.step_index = 0
            
        else:
            raise ValueError("Ugyldig mode. Brug 'full', 'half' eller et heltal (f.eks. 4, 8) for microstepping.")
    def set_step(self, step):
        for output, duty_cycle in zip(self.outputs, step):
            output.duty_u16(int(duty_cycle * 65535))
    def stop(self):
        for output in self.outputs:
            output.duty_u16(0)

    def move_stepper(self, steps, direction="forward", delay=0.01):
        # 1. Tjek om retningen findes
        if direction not in ["forward", "backward"]:
            raise ValueError("Fejl: Retningen skal være 'forward' eller 'backward'.")
            
        # 2. Gør negative skridt positive (normalisering)
        steps = abs(steps)
        
        # 3. Sæt en bundgrænse på forsinkelsen, f.eks. 0.002 sekunder
        if delay < 0.002:
            delay = 0.002
        sequence = self.modes[self.current_mode]
        if direction == "backward":
            sequence = list(reversed(sequence))
        try:
            for i in range(steps):
                step = sequence[i % len(sequence)]
                self.set_step(step)
            if direction == "forward":
                self.total_steps += steps
            else:
                self.total_steps -= steps
        finally:
            self.stop()
    def run_continuous(self, direction="forward", delay=0.01):
        print("Kører kontinuerligt... Tryk ctrl + c for at afbryde.")
        try:
            while True:
                self.move_stepper(8, direction=direction, delay=delay)
        except KeyboardInterrupt:
            print("\nRotation afbrudt.")
        finally:
            self.stop()
    def generate_microstep_sequence(self, microsteps):
        """
        Generate and return a complete microstep sequence.
        'microsteps' definerer antallet af brøkdele, et fuldt skridt deles op i.
        En komplet elektrisk cyklus består af 4 fulde skridt, så den samlede 
        sekvens vil indeholde (4 * microsteps) tilstande.
        """
        if not isinstance(microsteps, int) or microsteps < 1:
            raise ValueError("microsteps must be a positive integer")
        
        sequence = []
        
        # Vi finder max PWM-styrke ved at aflese den første værdi i full-step
        max_pwm = self.modes["full"][0][0]
        
        # En fuld elektrisk cyklus består af 4 magnetiske hovedskridt
        total_states = 4 * microsteps
        
        for i in range(total_states):
            # 1. Udregn vinklen i cirklen (i radianer)
            angle = (2 * math.pi * i) / total_states
            
            # 2. Udregn bølge-styrken for Spole A (sinus) og Spole B (cosinus)
            phase_a = math.sin(angle) * max_pwm
            phase_b = math.cos(angle) * max_pwm
            
            # 3. Opdel Spole A på A+ og A- benene
            if phase_a > 0:
                a_plus = phase_a
                a_minus = 0
            else:
                a_plus = 0
                a_minus = -phase_a  # Laver det negative tal om til positivt
                
            # 4. Opdel Spole B på B+ og B- benene
            if phase_b > 0:
                b_plus = phase_b
                b_minus = 0
            else:
                b_plus = 0
                b_minus = -phase_b  # Laver det negative tal om til positivt
                
            # 5. Tilføj dette mikroskridt til den endelige sekvens
            sequence.append([a_plus, b_plus, a_minus, b_minus])
            
        return sequence

