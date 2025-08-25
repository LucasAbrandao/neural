import pygame
import math

from sensors import Sensors

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

        # Sensores (ordem: começa esquerda e vai horário)
        self.sensors = Sensors(
            angles=[-90, -135, 180, 135, 90, 45, 0, -45]
        )

    def update(self, track_mask=None):
        keys = pygame.key.get_pressed()

        # Controle de aceleração
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed/2)
        else:
            # Atrito
            if self.speed > 0:
                self.speed -= 0.1
            elif self.speed < 0:
                self.speed += 0.1

        # Rotação
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed

        # Movimento baseado no ângulo
        rad = math.radians(self.angle)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)
        self.rect.x += dx
        self.rect.y += dy

        # Atualiza sprite rotacionado
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # inversão pra alinhar
        self.rect = self.image.get_rect(center=self.rect.center)

        # Atualiza máscara baseada na rotação
        self.mask = pygame.mask.from_surface(self.image)

        # Atualiza sensores
        if track_mask:
            self.sensors.update(self.angle, self.rect.center, track_mask)

    def draw(self, screen):
        # Desenha o carro
        screen.blit(self.image, self.rect.topleft)

        # Desenha sensores para debug
        self.sensors.draw(screen, self.angle, self.rect.center)
