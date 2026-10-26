from machine import ADC

adc = ADC(28)



while True:
    
    reading = adc.read_u16()
    print(reading)