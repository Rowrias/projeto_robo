import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template

from componentes.robo import Robo

app = Flask(__name__)
robo = Robo()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mover_frente')
def mover_frente():
    robo.mover_para_frente()
    return 'Movendo para frente!'

@app.route('/virar_esquerda')
def virar_esquerda():
    robo.virar_para_esquerda()
    return 'Virando para a esquerda!'

@app.route('/virar_direita')
def virar_direita():
    robo.virar_para_direita()
    return 'Virando para a direita!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
