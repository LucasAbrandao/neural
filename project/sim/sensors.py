import pygame
import math

class Sensors:
    def __init__(self, angles=None, max_length=0):
        # Lista de ângulos dos sensores (relativos à frente do carro)
        # Se não passar nada, usa padrão
        self.angles = angles if angles else [0, -45, 45, -90, 90, 135, -135, 180]

        # Distância máxima de cada sensor
        self.max_length = max_length

        # Lista que guarda as distâncias medidas
        self.distances = [max_length] * len(self.angles)

    def update(self, car_angle, car_pos, track_mask):
        self.distances = []

        for rel_angle in self.angles:
            # Ângulo absoluto (carro + relativo do sensor)
            angle = math.radians(car_angle + rel_angle)

            # Direção do sensor (vetor unitário)
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Testa ponto a ponto até bater em borda
            distance = 0
            x, y = car_pos
            while distance < self.max_length:
                test_x = int(x + dx * distance)
                test_y = int(y + dy * distance)

                # Verifica colisão com a pista (preto = fora da pista)
                if 0 <= test_x < track_mask.get_size()[0] and 0 <= test_y < track_mask.get_size()[1]:
                    if track_mask.get_at((test_x, test_y)) == 0:
                        break
                else:
                    break

                distance += 1

            self.distances.append(distance)

    def draw(self, screen, car_angle, car_pos):
        for i, rel_angle in enumerate(self.angles):
            angle = math.radians(car_angle + rel_angle)
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Ponto final baseado na distância medida
            end_x = car_pos[0] + dx * self.distances[i]
            end_y = car_pos[1] + dy * self.distances[i]

            # Linha do sensor
            pygame.draw.line(screen, (0, 255, 0), car_pos, (end_x, end_y), 2)

            # Ponto final
            pygame.draw.circle(screen, (255, 0, 0), (int(end_x), int(end_y)), 4)
