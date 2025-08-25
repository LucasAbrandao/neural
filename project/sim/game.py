import pygame

from car import Car
from track import Track

# Setup do pygame
pygame.init()

# Primeiro cria uma tela "temporária"
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Car + Track Simulation")

# Agora carrega a pista
track = Track("sprites/tracks/track1.png")

# Ajusta a janela para o tamanho exato da pista
screen = pygame.display.set_mode((track.width, track.height))

# Carrega o carro no centro da pista
car = Car(track.width // 2, track.height // 2)

clock = pygame.time.Clock()
running = True
collision_count = 0

# Nomes dos sensores (seguindo ordem horário a partir da esquerda)
sensor_names = [
    "Esquerda",
    "Trás-Esquerda",
    "Trás",
    "Trás-Direita",
    "Direita",
    "Frente-Direita",
    "Frente",
    "Frente-Esquerda",
]

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza carro com sensores ativos
    car.update(track.mask)

    # Desenha cena
    screen.fill((30, 30, 30))
    track.draw(screen)
    car.draw(screen)
    pygame.display.update()

    # Verifica colisão
    if track.check_collision(car):
        collision_count += 1
        print(f"⚠️ Car went off the track! {collision_count}")

    # Debug: printa valores dos sensores com nomes
    sensor_data = {name: int(dist) for name, dist in zip(sensor_names, car.sensors.distances)}
    print("Sensores (px):", sensor_data)

pygame.quit()
