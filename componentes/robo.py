# import RPi.GPIO as GPIO
from componentes.roda import Roda

class Robo:
    def __init__(self):
        # Instanciar as rodas com os pinos GPIO atribuídos
        self.roda_esquerda = Roda("esquerda", pino_frente=17, pino_tras=18)
        self.roda_direita  = Roda("direita",  pino_frente=22, pino_tras=23)

    def mover_para_frente(self):
        print("Movendo para frente")
        self.roda_esquerda.mover_para_frente()
        self.roda_direita.mover_para_frente()
        print("------------------------------------------------------------------------")

    def mover_para_tras(self):
        print("Movendo para tras")
        self.roda_esquerda.mover_para_tras()
        self.roda_direita.mover_para_tras()
        print("------------------------------------------------------------------------")

    def virar_para_esquerda(self):
        print("Virando para esquerda")
        self.roda_esquerda.mover_para_tras()
        self.roda_direita.mover_para_frente()
        print("------------------------------------------------------------------------")

    def virar_para_direita(self):
        print("Virando para direita")
        self.roda_esquerda.mover_para_frente()
        self.roda_direita.mover_para_tras()
        print("------------------------------------------------------------------------")

    def parar(self):
        print("Parando")
        self.roda_esquerda.parar()
        self.roda_direita.parar()
        print("------------------------------------------------------------------------")

    def cleanup(self):
        # GPIO.cleanup()
        # Chama o cleanup() de cada roda
        self.roda_esquerda.cleanup()
        self.roda_direita.cleanup()
        print("Limpeza de GPIO no Robo realizada.")
