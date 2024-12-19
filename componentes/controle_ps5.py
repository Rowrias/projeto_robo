import time
import pygame
from pygame.locals import *

from componentes import robo

class ControlePS5:
    def __init__(self, robo):
        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        self.conectado = False
        self.controle_ativo = False  # Define o estado inicial do controle ps5 como desconectado
        self.robo = robo

        self.mapeamento = { # Mapeamento dos botões e eixos
            "botoes": {
                0: "XIS",
                1: "BOLA",
                2: "QUADRADO",
                3: "TRIANGULO",
                4: "SELECT",
                5: "PLAYSTATION",
                6: "START",
                7: "L3",
                8: "R3",
                9: "L1",
                10: "R1",
                11: "SETA CIMA",
                12: "SETA BAIXO",
                13: "SETA ESQUERDA",
                14: "SETA DIREITA",
            },
            "eixos": {
                0: "HORIZONTAL ESQUERDO",           # Máximo para esquerda -1.0 e Máximo para direita 1.0
                1: "VERTICAL   ESQUERDO",           # Máximo para cima -1.0 e Máximo para baixo 1.0
                2: "HORIZONTAL DIREITO",            # Máximo para esquerda -1.0 e Máximo para direita 1.0
                3: "VERTICAL   DIREITO",            # Máximo para cima -1.0 e Máximo para baixo 1.0
                4: "L2",                            # começa -1.0 e vai até quase 1.0
                5: "R2",                            # começa -1.0 e vai até quase 1.0
            }
        }

        # Limiar de ativação e desativação (quando o movimento é considerado significativo)
        self.dead_zone = 0.2                                    # Valor para considerar o eixo neutro (quando ele deve parar)
        self.analogico_ativacao_positive = self.dead_zone       # Valor para considerar um movimento significativo
        self.analogico_ativacao_negative = 0 - self.dead_zone   # Valor para considerar um movimento significativo

        self.eixo_estado = {  # Estado do eixo para saber se está em movimento ou não
            "HORIZONTAL ESQUERDO": False,
            "VERTICAL   ESQUERDO": False,
            "HORIZONTAL DIREITO": False,
            "VERTICAL   DIREITO": False
        }

    def conectar(self):
        """
        Conecta o joystick ao sistema. 
        Reinicia a configuração caso seja reconectado.
        """
        pygame.joystick.quit()  # Finaliza qualquer joystick ativo
        pygame.joystick.init()  # Reinicia o subsistema de joystick

         # Verifica e inicializa o Pygame caso necessário
        if not pygame.get_init():
            pygame.init()  # Inicializa o Pygame novamente
            print("Pygame reiniciado.")

        pygame.joystick.quit()  # Finaliza qualquer joystick ativo
        pygame.joystick.init()  # Reinicia o subsistema de joystick
        if pygame.joystick.get_count() > 0:  # Verifica se há joysticks conectados
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.conectado = True
            print(f"Controle {self.joystick.get_name()} conectado.")
        else:
            self.conectado = False
            print("Nenhum controle conectado.")


    def ler_comandos(self):
        """
        Captura os eventos do controle e retorna uma lista de ações 
        correspondentes aos botões ou eixos.
        """
        if not self.conectado:
            return []
        
        comandos = []
        try:
        # Certifique-se de que o pygame esteja inicializado antes de capturar eventos
            if pygame.get_init():
                for event in pygame.event.get():
                    if event.type == JOYBUTTONDOWN:  # Botões pressionados
                        botao = event.button
                        nome_botao = self.mapeamento["botoes"].get(botao, f"BOTAO {botao}")
                        comandos.append(f"BOTAO PRESSIONADO: {nome_botao}")

                    elif event.type == JOYBUTTONUP:  # Botões soltos
                        botao = event.button
                        nome_botao = self.mapeamento["botoes"].get(botao, f"BOTAO {botao}")
                        comandos.append(f"BOTAO SOLTO: {nome_botao}")

                    elif event.type == JOYAXISMOTION:
                        pygame.event.pump()
                        for i in range(self.joystick.get_numaxes()):
                            nome_eixo = self.mapeamento["eixos"].get(i, f"EIXO {i}")
                            axis_value = round(self.joystick.get_axis(i), 1)

                            if abs(axis_value) > self.analogico_ativacao_positive or abs(axis_value) < self.analogico_ativacao_negative:
                                self.eixo_estado[nome_eixo] = True
                            elif abs(axis_value) <= self.dead_zone:
                                self.eixo_estado[nome_eixo] = False

                            # Verificar se o eixo pertence ao analógico esquerdo
                            if nome_eixo == "HORIZONTAL ESQUERDO" or nome_eixo == "VERTICAL ESQUERDO":
                                horizontal_value = round(self.joystick.get_axis(0), 1)
                                vertical_value = round(self.joystick.get_axis(1), 1)

                                if abs(horizontal_value) > self.dead_zone or abs(vertical_value) > self.dead_zone:
                                    horizontal_status = "A" if abs(horizontal_value) > self.dead_zone else "D"
                                    vertical_status = "A" if abs(vertical_value) > self.dead_zone else "D"

                                    print(f"HORIZONTAL ESQUERDO: {horizontal_value} ({horizontal_status}) | VERTICAL   ESQUERDO: {vertical_value} ({vertical_status})")
                            
                            # Verificar se o eixo pertence ao analógico direito
                            elif nome_eixo == "HORIZONTAL DIREITO" or nome_eixo == "VERTICAL DIREITO":
                                horizontal_value_direito = round(self.joystick.get_axis(2), 1)
                                vertical_value_direito = round(self.joystick.get_axis(3), 1)

                                # Verifica se o valor do eixo é maior que 0.2 antes de imprimir
                                if abs(horizontal_value_direito) > self.dead_zone or abs(vertical_value_direito) > self.dead_zone:
                                    horizontal_status_direito = "A" if abs(horizontal_value_direito) > self.dead_zone else "D"
                                    vertical_status_direito = "A" if abs(vertical_value_direito) > self.dead_zone else "D"
                                    print(f"HORIZONTAL DIREITO: {horizontal_value_direito} ({horizontal_status_direito}) | VERTICAL   DIREITO: {vertical_value_direito} ({vertical_status_direito})")

                            # Verificar o eixo L2
                            elif nome_eixo == "L2":
                                eixo_l2 = round(self.joystick.get_axis(4), 1)
                                if abs(eixo_l2) > -1.0 and abs(eixo_l2) < 1.0:
                                    print(f"L2: {eixo_l2}")

                            # Verificar o eixo R2
                            elif nome_eixo == "R2":
                                eixo_r2 = round(self.joystick.get_axis(5), 1)
                                if abs(eixo_r2) > -1.0 and abs(eixo_r2) < 1.0:
                                    print(f"R2: {eixo_r2}")

        except pygame.error as e:
            print(f"Erro ao processar eventos: {e}")
            self.desconectar()

        return comandos
    
    def comandos(self):
        comando_lidos = self.ler_comandos()
        for comando_lido in comando_lidos: # Processa os eventos lidos
                print(f"* {comando_lido}")

                # Alterna o controle 'ativo' ou 'inativo'
                if comando_lido == 'BOTAO PRESSIONADO: SELECT':
                    self.controle_ativo = not self.controle_ativo
                    estado = "ativo" if self.controle_ativo else "inativo"
                    print(f"Controle alternado para estado: {estado}.")
                    continue # Volta para o início do loop

                # Controle do robô SOMENTE se o controle estiver ativo
                if self.controle_ativo:

                    # Eixos do controle analogico esquerdo
                    if 'EIXO HORIZONTAL ESQUERDO' in comando_lido or 'EIXO VERTICAL   ESQUERDO' in comando_lido:
                        horizontal = float(comando_lido.split(":")[1].strip()) if 'HORIZONTAL ESQUERDO' in comando_lido else 0
                        vertical = float(comando_lido.split(":")[1].strip()) if 'VERTICAL   ESQUERDO' in comando_lido else 0

                        # Movimentos simples
                        if vertical < self.analogico_ativacao_negative:
                            print("Movendo para frente.")
                            robo.mover_para_frente(velocidade=1.0)

                        elif vertical > self.analogico_ativacao_positive:
                            print("Movendo para trás.")
                            robo.mover_para_tras(velocidade=1.0)

                        elif horizontal < -0.3:
                            print("Virando para esquerda.")
                            robo.virar_para_esquerda(velocidade=1.0)

                        elif horizontal > 0.3:
                            print("Virando para direita.")
                            robo.virar_para_direita(velocidade=1.0)
                        
                        # Movimento em diagonal para frente
                        elif vertical < -0.3 and horizontal < -0.3:
                            print("Movendo para frente e esquerda (diagonal).")
                            robo.mover_para_frente(velocidade=0.7)
                            robo.virar_para_esquerda(velocidade=0.7)

                        elif vertical < -0.3 and horizontal > 0.3:
                            print("Movendo para frente e direita (diagonal).")
                            robo.mover_para_frente(velocidade=0.7)
                            robo.virar_para_direita(velocidade=0.7)

                        # Movimento em diagonal para trás
                        elif vertical > 0.3 and horizontal < -0.3:
                            print("Movendo para trás e esquerda (diagonal).")
                            robo.mover_para_tras(velocidade=0.7)
                            robo.virar_para_esquerda(velocidade=0.7)

                        elif vertical > 0.3 and horizontal > 0.3:
                            print("Movendo para trás e direita (diagonal).")
                            robo.mover_para_tras(velocidade=0.7)
                            robo.virar_para_direita(velocidade=0.7)

                        # Parada do movimento
                        else:
                            print("Parando o movimento.")
                            robo.parar()


                    # Eixos do controle analogico direito
                    elif 'EIXO HORIZONTAL DIREITO' in comando_lido:
                        axis_value = float(comando_lido.split(":")[1].strip())
                        if axis_value < self.analogico_ativacao_negative:
                            print("Movimento no eixo horizontal direito detectado, mas sem ação definida.")
                        elif axis_value > self.analogico_ativacao_positive:
                            print("Movimento no eixo horizontal direito detectado, mas sem ação definida.")

                    elif 'EIXO VERTICAL   DIREITO' in comando_lido:
                        axis_value = float(comando_lido.split(":")[1].strip())
                        if axis_value < self.analogico_ativacao_negative:
                            print("Movimento no eixo vertical direito detectado, mas sem ação definida.")
                        elif axis_value > self.analogico_ativacao_positive:
                            print("Movimento no eixo vertical direito detectado, mas sem ação definida.")
                    
                    
                    # Botão do controle
                    elif comando_lido == 'BOTAO PRESSIONADO: XIS':
                        print("Botão XIS pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: BOLA':
                        print("Botão BOLA pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: QUADRADO':
                        print("Botão QUADRADO pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: TRIANGULO':
                        print("Botão TRIANGULO pressionado, mas sem ação definida.")

                    elif comando_lido == 'BOTAO PRESSIONADO: PLAYSTATION':
                        self.desconectar() # Desconecta o controle
                        print("Controle desconectado.")
                        print("...")
                        time.sleep(2)

                    elif comando_lido == 'BOTAO PRESSIONADO: START': # Finalizar programa 
                        print("Finalizando execução do robô.")
                        break # Encerra o Loop

                    elif comando_lido == 'BOTAO PRESSIONADO: L3':
                        print("Botão L3 pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: R3':
                        print("Botão R3 pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: L1':
                        print("Botão L1 pressionado, mas sem ação definida.")
                    elif comando_lido == 'BOTAO PRESSIONADO: R1':
                        print("Botão R1 pressionado, mas sem ação definida.")

                    elif comando_lido == 'BOTAO PRESSIONADO: SETA CIMA':
                        self.robo.mover_para_frente()  # Inicia o movimento
                    elif comando_lido == 'BOTAO SOLTO: SETA CIMA':
                        self.robo.parar()  # Para o movimento

                    elif comando_lido == 'BOTAO PRESSIONADO: SETA BAIXO':
                        self.robo.mover_para_tras()  # Inicia o movimento
                    elif comando_lido == 'BOTAO SOLTO: SETA BAIXO':
                        self.robo.parar()  # Para o movimento

                    elif comando_lido == 'BOTAO PRESSIONADO: SETA ESQUERDA':
                        self.robo.virar_para_esquerda()  # Inicia o movimento
                    elif comando_lido == 'BOTAO SOLTO: SETA ESQUERDA':
                        self.robo.parar()  # Para o movimento

                    elif comando_lido == 'BOTAO PRESSIONADO: SETA DIREITA':
                        self.robo.virar_para_direita()  # Inicia o movimento
                    elif comando_lido == 'BOTAO SOLTO: SETA DIREITA':
                        self.robo.parar()  # Para o movimento

                time.sleep(0.1)  # Pequeno intervalo no loop para reduzir uso da CPU
    
    def desconectar(self):
        pygame.quit() # Encerra o pygame
        self.joystick = None # desliga o controle
        self.conectado = False # não há controle conectado
        print("Controle PS5 desconectado!!!")
