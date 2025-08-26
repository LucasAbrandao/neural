import pygame
import math
import csv
import os

from sensors import Sensors
from nn.policy import CarPolicy  # controlador NN


class Car:
    def __init__(self, x, y):
        # Carrega sprite
        self.original_image = pygame.image.load("sprites/carModels/carF1.png").convert_alpha()

        # Escala o carro para um tamanho mais razoável (90x54 mantém proporção ~50/30)
        self.original_image = pygame.transform.scale(self.original_image, (90, 54))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Máscara inicial
        self.mask = pygame.mask.from_surface(self.image)

        # Movimento
        self.angle = 0   # ângulo inicial
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 5
        self.rotation_speed = 5

        # Sensores
        self.sensors = Sensors(
            angles=[-90, -135, 180, 135, 90, 45, 0, -45]
        )

        # IA (opcional)
        self.policy = CarPolicy(input_size=len(self.sensors.angles))
        self.use_ai = False

        # Logging
        self.log_data = True
        self.logfile = "data/driving_log.csv"
        os.makedirs("data", exist_ok=True)
        if self.log_data and not os.path.exists(self.logfile):
            with open(self.logfile, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([f"s{i}" for i in range(len(self.sensors.angles))] + ["action"])

    def update(self, track_mask=None):
        if self.use_ai and track_mask:
            # Normaliza sensores
            inputs = [min(d, 300) / 300 for d in self.sensors.distances]
            action, _ = self.policy.act(inputs)
            self.apply_action(action)
        else:
            action = self.manual_control()

            # Loga dados de treino
            if self.log_data and track_mask:
                inputs = [min(d, 300) / 300 for d in self.sensors.distances]
                with open(self.logfile, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(inputs + [action])

        # Movimento baseado no ângulo
        rad = math.radians(self.angle)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)
        self.rect.x += dx
        self.rect.y += dy

        # Atualiza sprite rotacionado
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Atualiza máscara
        self.mask = pygame.mask.from_surface(self.image)

        # Atualiza sensores
        if track_mask:
            self.sensors.update(self.angle, self.rect.center, track_mask)

    def manual_control(self):
        keys = pygame.key.get_pressed()
        action = 0  # nada

        # Controle de aceleração
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
            action = 1
        elif keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
            action = 2
        else:
            # Atrito
            if self.speed > 0:
                self.speed -= 0.1
            elif self.speed < 0:
                self.speed += 0.1

        # Rotação
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
            action = 3 if action == 0 else 5
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed
            action = 4 if action == 0 else 6

        return action

    def apply_action(self, action):
        """Mapeia as 9 ações da rede neural para comandos do carro."""
        if action in [1, 5, 6]:   # acelerar
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif action in [2, 7, 8]: # dar ré
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:  # nada → atrito
            if self.speed > 0:
                self.speed -= 0.05
            if self.speed < 0:
                self.speed += 0.05

        if action in [3, 5, 7]:   # virar esquerda
            self.angle -= self.rotation_speed
        if action in [4, 6, 8]:   # virar direita
            self.angle += self.rotation_speed

    def draw(self, screen):
        # Desenha o carro
        screen.blit(self.image, self.rect.topleft)
        # Desenha sensores para debug
        self.sensors.draw(screen, self.angle, self.rect.center)
