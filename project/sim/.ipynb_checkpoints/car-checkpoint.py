import pygame
import math

# Initialize pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Simulation")

# Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.width = 40
        self.height = 20

    def draw(self, screen):
        # Draw the car as a rotated rectangle
        car_rect = pygame.Rect(0, 0, self.width, self.height)
        car_rect.center = (self.x, self.y)

        car_surface = pygame.Surface((self.width, self.height))
        car_surface.fill((0, 255, 0))
        rotated_car = pygame.transform.rotate(car_surface, -math.degrees(self.angle))
        rect = rotated_car.get_rect(center=car_rect.center)
        screen.blit(rotated_car, rect.topleft)

    def move(self, forward=True):
        if forward:
            self.speed = 2
        else:
            self.speed = 0

        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def rotate(self, right=True):
        if right:
            self.angle += 0.05
        else:
            self.angle -= 0.05


# Main loop
car = Car(400, 300)
running = True
clock = pygame.time.Clock()

while running:
    window.fill((0, 0, 0))  # black background

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.move(True)
    if keys[pygame.K_LEFT]:
        car.rotate(False)
    if keys[pygame.K_RIGHT]:
        car.rotate(True)

    # Draw the car
    car.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
