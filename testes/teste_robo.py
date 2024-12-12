import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from componentes.robo import Robo

robo1 = Robo()
robo2 = Robo()

robo1.mover_para_frente()
robo2.mover_para_tras()
