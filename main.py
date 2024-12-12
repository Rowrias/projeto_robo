import time

import pygame
from componentes.robo import Robo
# from componentes.controle_teclado import ControleTeclado
from componentes.controle_ps5 import ControlePS5

def controle_robo():
    robo = Robo()
    # controle_teclado = ControleTeclado(robo)
    controle_ps5 = ControlePS5()
    controle_ativo = False  # Define o estado inicial do controle ps5 como desconectado

    try:
        print("Iniciando o main.py --> controle_robo() ...")

        # controle_teclado.conectar()  # Inicia o controle de teclado

        running = True
        while running: # Loop principal
            
            if not controle_ps5.conectado:
                try:
                    print("Tentando reconectar o controle...")
                    controle_ps5.conectar()
                except pygame.error as e:
                    print(f"Erro ao reconectar o controle PS5: {e}")
                    if "video system not initialized" in str(e):
                        pygame.init()  # Reinicializa todos os subsistemas do Pygame
                        print("Subsistema de vídeo do Pygame reiniciado.")
                    time.sleep(5)
                    continue

            if not controle_ps5.conectado: # Se o controle não estiver conectado ...
                print("Aguardando conexão do controle PS5...")
                print("...")
                time.sleep(5) # Aguarda 2 segundos antes de tentar novamente
                continue # Volta para o início do loop    
            
            eventos_lidos = controle_ps5.ler_eventos()

            for evento_lido in eventos_lidos: # Processa os eventos lidos
                print(f"* {evento_lido}")

                # Alterna conexão com o controle 'ativo' ou 'inativo'
                if evento_lido == 'BOTAO PRESSIONADO: SELECT':
                    controle_ativo = not controle_ativo
                    estado = "ativo" if controle_ativo else "inativo"
                    print(f"Controle alternado para estado: {estado}.")
                    continue # Volta para o início do loop

                # Controle do robô SOMENTE se o controle estiver ativo
                if controle_ativo == True:

                    # Eixos do controle analogico esquerdo
                    if 'EIXO HORIZONTAL ESQUERDO' in evento_lido:
                        axis_value = float(evento_lido.split(":")[1].strip())
                        if axis_value < -0.3:
                            robo.virar_para_esquerda()
                        elif axis_value > 0.3:
                            robo.virar_para_direita()

                    elif 'EIXO VERTICAL   ESQUERDO' in evento_lido:
                        axis_value = float(evento_lido.split(":")[1].strip())
                        if axis_value < -0.3:
                            robo.mover_para_frente()
                        elif axis_value > 0.3:
                            robo.mover_para_tras()

                    # Eixos do controle analogico direito
                    elif 'EIXO HORIZONTAL DIREITO' in evento_lido:
                        axis_value = float(evento_lido.split(":")[1].strip())
                        if axis_value < -0.3:
                            print("Movimento no eixo horizontal direito detectado, mas sem ação definida.")
                        elif axis_value > 0.3:
                            print("Movimento no eixo horizontal direito detectado, mas sem ação definida.")

                    elif 'EIXO VERTICAL   DIREITO' in evento_lido:
                        axis_value = float(evento_lido.split(":")[1].strip())
                        if axis_value < -0.2:
                            print("Movimento no eixo vertical direito detectado, mas sem ação definida.")
                        elif axis_value > 0.2:
                            print("Movimento no eixo vertical direito detectado, mas sem ação definida.")
                    
                    
                    # Botão do controle
                    elif evento_lido == 'BOTAO PRESSIONADO: XIS':
                        print("Botão XIS pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: BOLA':
                        print("Botão BOLA pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: QUADRADO':
                        print("Botão QUADRADO pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: TRIANGULO':
                        print("Botão TRIANGULO pressionado, mas sem ação definida.")

                    elif evento_lido == 'BOTAO PRESSIONADO: PLAYSTATION':
                        controle_ps5.desconectar() # Desconecta o controle
                        print("Controle desconectado.")
                        print("...")
                        time.sleep(2)
                    elif evento_lido == 'BOTAO PRESSIONADO: START': # Finalizar programa 
                        print("Finalizando execução do robô.")
                        running = False
                        break # Encerra o Loop

                    elif evento_lido == 'BOTAO PRESSIONADO: L3':
                        print("Botão L3 pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: R3':
                        print("Botão R3 pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: L1':
                        print("Botão L1 pressionado, mas sem ação definida.")
                    elif evento_lido == 'BOTAO PRESSIONADO: R1':
                        print("Botão R1 pressionado, mas sem ação definida.")

                    elif evento_lido == 'BOTAO PRESSIONADO: SETA CIMA':
                        robo.mover_para_frente()  # Inicia o movimento
                    elif evento_lido == 'BOTAO SOLTO: SETA CIMA':
                        robo.parar()  # Para o movimento

                    elif evento_lido == 'BOTAO PRESSIONADO: SETA BAIXO':
                        robo.mover_para_tras()  # Inicia o movimento
                    elif evento_lido == 'BOTAO SOLTO: SETA BAIXO':
                        robo.parar()  # Para o movimento

                    elif evento_lido == 'BOTAO PRESSIONADO: SETA ESQUERDA':
                        robo.virar_para_esquerda()  # Inicia o movimento
                    elif evento_lido == 'BOTAO SOLTO: SETA ESQUERDA':
                        robo.parar()  # Para o movimento

                    elif evento_lido == 'BOTAO PRESSIONADO: SETA DIREITA':
                        robo.virar_para_direita()  # Inicia o movimento
                    elif evento_lido == 'BOTAO SOLTO: SETA DIREITA':
                        robo.parar()  # Para o movimento

                time.sleep(0.1)  # Pequeno intervalo no loop para reduzir uso da CPU

    finally:
        robo.cleanup() # limpa o GPIO
        # controle_teclado.desconectar()
        controle_ps5.desconectar() # Desconecta o controle
        print("Programa finalizado.")

if __name__ == "__main__":
    try:
        print("Iniciando o programa")
        controle_robo()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
