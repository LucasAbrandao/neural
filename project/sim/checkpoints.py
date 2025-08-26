# project/sim/checkpoints.py
import pygame

class Checkpoints:
    def __init__(self, points):
        """
        points: lista de coordenadas (x, y) para checkpoints
        """
        self.points = points
        self.radius = 40  # raio de tolerância

        # controle de qual é o próximo alvo
        self.current_index = 0

    def draw(self, screen):
        for i, (x, y) in enumerate(self.points):
            color = (0, 255, 0) if i == self.current_index else (255, 0, 0)
            pygame.draw.circle(screen, color, (x, y), self.radius, 2)

    def check_passed(self, car_pos):
        """
        Retorna True se o carro passou pelo checkpoint correto
        """
        cx, cy = self.points[self.current_index]
        dx = car_pos[0] - cx
        dy = car_pos[1] - cy
        dist2 = dx * dx + dy * dy
        if dist2 <= self.radius * self.radius:
            self.current_index = (self.current_index + 1) % len(self.points)
            return True
        return False
