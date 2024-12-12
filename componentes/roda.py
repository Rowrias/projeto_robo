# import RPi.GPIO as GPIO
# import time

class Roda:
    def __init__(self, lado, pino_frente, pino_tras):
        self.lado = lado
        self.pino_frente = pino_frente
        self.pino_tras = pino_tras

        ## Configurar os pinos GPIO
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.pino_frente, GPIO.OUT)
        # GPIO.setup(self.pino_tras, GPIO.OUT)

    def mover_para_frente(self):
        # GPIO.output(self.pino_frente, GPIO.HIGH)
        # GPIO.output(self.pino_tras, GPIO.LOW)
        print(f"  -- Roda {self.lado} movendo para 'frente'.")

    def mover_para_tras(self):
        # GPIO.output(self.pino_frente, GPIO.LOW)
        # GPIO.output(self.pino_tras, GPIO.HIGH)
        print(f"  -- Roda {self.lado} movendo para 'trás'.")

    def parar(self):
        #GPIO.output(self.pino_frente, GPIO.LOW)
        # GPIO.output(self.pino_tras, GPIO.LOW)
        print(f"  -- Roda {self.lado} 'parada'.")

    def cleanup(self):
        ## Limpar os pinos configurados
        #GPIO.cleanup()
        print(f"Limpeza de GPIO na Roda {self.lado} realizada.")