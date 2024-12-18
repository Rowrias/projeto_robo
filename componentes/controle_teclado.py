from pynput import keyboard

class ControleTeclado:
    def __init__(self, robo):
        self.listener = None
        self.robo = robo  # Passa o objeto robo para controlar diretamente
        self.controle_ativo = False  # Variável para ativar/desativar o controle
        self.teclas_pressionadas = set()  # Para rastrear teclas pressionadas
        self.em_movimento = False  # Estado do robô (em movimento ou parado)


    def conectar(self):
        """Inicia o listener de teclado"""
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Controle teclado conectado!!!")

    def on_press(self, key):
        """Ações ao pressionar a tecla"""
        try:
            if key == keyboard.Key.pause:
                self.controle_ativo = not self.controle_ativo
                estado = "ativo" if self.controle_ativo else "desativado"
                print(f"Controle teclado {estado}!")

            # Se o controle estiver ativo, processa as teclas
            if self.controle_ativo:
                if hasattr(key, 'char') and key.char:
                    # Só adiciona teclas de movimento
                    if key.char in ['w', 'a', 's', 'd']:
                        self.teclas_pressionadas.add(key.char)
                        if key.char == 'w':
                            self.robo.mover_para_frente()
                        elif key.char == 's':
                            self.robo.mover_para_tras()
                        elif key.char == 'a':
                            self.robo.virar_para_esquerda()
                        elif key.char == 'd':
                            self.robo.virar_para_direita()
                        
                        # O robô está em movimento agora
                        self.em_movimento = True

                elif key == keyboard.Key.space:
                    print("Espaço pressionado - exemplo: tirou foto!")
                    
        except AttributeError:
            pass  # Ignora teclas não tratadas

    def on_release(self, key):
        """Ações ao soltar a tecla"""
        try:
            if self.controle_ativo:
                # Se a tecla for uma tecla de movimento, remove do conjunto
                if hasattr(key, 'char') and key.char:
                    self.teclas_pressionadas.remove(key.char)

                # O robô só deve parar se **todas as teclas de movimento** forem soltas
                if not any(k in self.teclas_pressionadas for k in ['w', 'a', 's', 'd']):
                    # Só chama parar() se o robô estava em movimento
                    if self.em_movimento:
                        self.robo.parar()
                        self.em_movimento = False  # O robô está parado agora
                    else:
                        print("------------------------------------------------------------------------")

        except AttributeError:
            pass  # Ignora teclas não tratadas

    def desconectar(self):
        """Desconecta o listener do teclado"""
        if self.listener:
            self.listener.stop()
        print("Controle teclado desconectado!!!")
