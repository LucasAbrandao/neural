import pygame
import math

class Sensors:
    def __init__(self, angles, length=1000):
        """
        angles: lista de ângulos relativos em graus
        length: alcance máximo do sensor
        """
        self.angles = angles
        self.length = length
        self.distances = [length for _ in angles]  # inicia max range

    def update(self, car_angle, car_pos, track_mask):
        """
        Atualiza as distâncias detectadas pelos sensores.
        """
        cx, cy = car_pos
        self.distances = []

        for a in self.angles:
            angle = math.radians(car_angle + a)
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Avança pixel a pixel até bater ou sair do range
            dist = 0
            while dist < self.length:
                x = int(cx + dx * dist)
                y = int(cy + dy * dist)

                if (0 <= x < track_mask.get_size()[0]) and (0 <= y < track_mask.get_size()[1]):
                    if track_mask.get_at((x, y)) == 0:  # preto = fora da pista
                        break
                else:
                    break
                dist += 1

            self.distances.append(dist)

    def draw(self, screen, car_angle, car_pos):
        """
        Renderiza as linhas e pontos dos sensores.
        """
        cx, cy = car_pos
        for i, a in enumerate(self.angles):
            angle = math.radians(car_angle + a)
            dist = self.distances[i]

            x2 = int(cx + math.cos(angle) * dist)
            y2 = int(cy + math.sin(angle) * dist)

            # linha vermelha
            pygame.draw.line(screen, (255, 0, 0), (cx, cy), (x2, y2), 2)
            # bolinha amarela na ponta
            pygame.draw.circle(screen, (255, 255, 0), (x2, y2), 4)
