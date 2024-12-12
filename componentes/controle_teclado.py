from pynput import keyboard

class ControleTeclado:
    def __init__(self, robo):
        self.listener = None
        self.robo = robo  # Passa o objeto robo para controlar diretamente

    def conectar(self):
        """Inicia o listener de teclado"""
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        """Ações ao pressionar a tecla"""
        try:
            if key == keyboard.Key.up:
                self.robo.mover_para_frente()
            elif key == keyboard.Key.down:
                self.robo.mover_para_tras()
            elif key == keyboard.Key.left:
                self.robo.virar_para_esquerda()
            elif key == keyboard.Key.right:
                self.robo.virar_para_direita()
            elif key == keyboard.Key.esc:
                print("Finalizando execução do robô.")
                return False  # Finaliza o programa
        except AttributeError:
            pass  # Ignora teclas especiais ou não tratadas

    def on_release(self, key):
        """Ações ao soltar a tecla"""
        pass

    def desconectar(self):
        """Desconecta o listener do teclado"""
        if self.listener:
            self.listener.stop()
