import numpy as np

try:
    # quando rodado como módulo (-m sim.game)
    from .model import Model
    from .layers import Dense
    from .activations import ReLU, Softmax
except ImportError:
    # quando rodado direto (python3 game.py)
    from nn.model import Model
    from nn.layers import Dense
    from nn.activations import ReLU, Softmax


class CarPolicy:
    def __init__(self, input_size=9, hidden_size=12, output_size=9):
        # rede simples: sensores -> camada oculta -> ações
        self.model = Model([
            Dense(input_size, hidden_size),
            ReLU(),
            Dense(hidden_size, output_size),
            Softmax()
        ])

    def act(self, sensor_values):
        """
        Recebe lista com distâncias dos sensores (normalizadas)
        Retorna índice da ação escolhida
        """
        x = np.array(sensor_values).reshape(1, -1)
        probs = self.model.forward(x)
        action = np.argmax(probs)
        return action, probs
