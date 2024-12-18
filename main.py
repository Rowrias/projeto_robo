import time

import pygame
from componentes.robo import Robo
from componentes.controle_teclado import ControleTeclado
from componentes.controle_ps5 import ControlePS5

def controle_robo():
    robo = Robo()
    controle_teclado = ControleTeclado(robo)
    controle_ps5 = ControlePS5(robo)
    
    try:
        print("Iniciando o main.py --> controle_robo() ...")

        controle_teclado.conectar()  # Inicia o controle de teclado

        while True: # Loop principal
            
            if not controle_ps5.conectado:
                print("Tentando reconectar o controle...")
                controle_ps5.conectar()
                if not controle_ps5.conectado:
                    print("Aguardando conexão do controle PS5...")
                    print("...")
                    time.sleep(5)
                    continue

            # Loop dos comandos do PS5
            controle_ps5.comandos()

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")

    finally:
        robo.cleanup() # limpa o GPIO
        controle_teclado.desconectar() # Desconecta o teclado
        controle_ps5.desconectar() # Desconecta o controle
        print("Programa finalizado.")

if __name__ == "__main__":
    controle_robo()
