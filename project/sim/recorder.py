# project/sim/recorder.py
import csv
import os
from datetime import datetime

class Recorder:
    def __init__(self, save_dir="data"):
        # cria pasta de dados se não existir
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(save_dir, f"session_{timestamp}.csv")

        # abre arquivo para escrita
        self.file = open(self.filepath, "w", newline="")
        self.writer = csv.writer(self.file)

        # cabeçalho
        header = ["time", "x", "y"] + [f"sensor_{i}" for i in range(9)] + ["action"]
        self.writer.writerow(header)

        print(f"🎥 Gravando dados em {self.filepath}")

    def record(self, time_ms, car, sensors, action):
        """
        Grava um passo da simulação
        - time_ms: tempo atual em ms (pygame.time.get_ticks())
        - car: objeto Car (para pegar posição)
        - sensors: lista de valores de sensores
        - action: ação tomada (ex: string ou int)
        """
        row = [time_ms, car.rect.centerx, car.rect.centery] + list(sensors) + [action]
        self.writer.writerow(row)

    def close(self):
        self.file.close()
        print(f"💾 Dados salvos em {self.filepath}")
