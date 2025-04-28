import RPi.GPIO as GPIO
import time
import threading

class SwitchCounter:
    def __init__(self, sensor_id: str, pin: int) -> None:
        """
        # Switch Counter Class
        Questa classe serve per gestire un contatore associato ad un sensore identificato da un ID e collegato a un pin GPIO.

        ### Args:
        - sensor_id : str : identificativo del sensore (es. nome azienda o codice)
        - pin : int : il numero del pin GPIO associato al sensore
        """
        self.sensor_id = sensor_id
        self.pin = pin
        self.counter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self) -> None:
        """
        Avvia il contatore che incrementa ogni volta che il sensore viene attivato.

        ### Return:
        - None
        """
        print(f"Contatore avviato per sensore '{self.sensor_id}' su pin GPIO{self.pin}.")

        try:
            while True:
                if GPIO.input(self.pin) == GPIO.LOW:
                    self.counter += 1
                    print(f"[{self.sensor_id}] Conteggio: {self.counter}")
                    while GPIO.input(self.pin) == GPIO.LOW:
                        time.sleep(0.01)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print(f"\nTerminato il conteggio per '{self.sensor_id}'")

 
PIN_USED = [17, 18]  

sensors = []
for idx, pin in enumerate(PIN_USED, start=1):
    sensor = SwitchCounter(f"azienda_{idx}", pin)
    sensors.append(sensor)


threads = []
for sensor in sensors:
    thread = threading.Thread(target=sensor.run)
    thread.start()
    threads.append(thread)

