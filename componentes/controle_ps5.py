import pygame
from pygame.locals import *

class ControlePS5:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        self.conectado = False

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
        self.analogico_ativacao_positive = 0.3     # Valor para considerar um movimento significativo
        self.analogico_ativacao_negative = -0.3    # Valor para considerar um movimento significativo
        self.dead_zone_positive = 0.1       # Valor para considerar o eixo neutro (quando ele deve parar)
        self.dead_zone_negative = -0.1      # Valor para considerar o eixo neutro (quando ele deve parar)

        self.eixo_estado = {  # Estado do eixo para saber se está em movimento ou não
            "HORIZONTAL ESQUERDO": False,
            "VERTICAL   ESQUERDO": False,
            "HORIZONTAL DIREITO": False,
            "VERTICAL   DIREITO": False
        }

    def conectar(self):
        """
        Conecta o joystick ao sistema. Reinicia a configuração caso seja reconectado.
        """

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
            pygame.event.pump()  # Limpa eventos antigos do pygame
            print(f"Controle {self.joystick.get_name()} conectado.")

        else:
            self.conectado = False
            print("Nenhum controle conectado.")


    def ler_eventos(self):
        """
        Captura os eventos do controle e retorna uma lista de ações correspondentes aos botões ou eixos.
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

                    elif event.type == JOYAXISMOTION:  # Movimento dos eixos
                        eixo = event.axis
                        axis_value = round(self.joystick.get_axis(eixo), 2)  # Arredonda para 2 casas

                        nome_eixo = self.mapeamento["eixos"].get(eixo, f"EIXO {eixo}")
                        
                        if abs(axis_value) > self.analogico_ativacao_positive or abs(axis_value) < self.analogico_ativacao_negative:  # Se o valor for grande o suficiente
                            # Ativa o movimento no eixo
                            if not self.eixo_estado[nome_eixo]:
                               self.eixo_estado[nome_eixo] = True
                            # Imprime os valores dos eixos
                            # print(f"Eixo acima do dead zone =")
                            print(f"EIXO {nome_eixo}: {axis_value}")

                        if abs(axis_value) <= self.dead_zone_positive and self.eixo_estado.get(nome_eixo):
                            # Se o eixo estiver no "neutro" e estava ativado, desativa o movimento
                            self.eixo_estado[nome_eixo] = False
                            # Imprime os valores dos eixos
                            print(f"Eixo abaixo do dead zone = Desativado")
                            
        except pygame.error as e:
            print(f"Erro ao processar eventos: {e}")
            self.desconectar()

        return comandos

    def desconectar(self):
        pygame.quit() # Encerra o pygame
        self.joystick = None # desliga o controle
        self.conectado = False # não há controle conectado
        print("Controle PS5 desconectado!!!")
