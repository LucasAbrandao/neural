import pygame
import math

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Simulation")

# select Load car image

# car_image = pygame.image.load("sprites/carModels/carYellow.png")   
# car_image = pygame.transform.scale(car_image, (100, 60))  

car_image = pygame.image.load("sprites/carModels/carF1.png")   
car_image = pygame.transform.scale(car_image, (100, 80))  

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.image = car_image
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed = 5
        else:
            self.speed = 0
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        # Atualiza posição
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)

    def draw(self, win):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        win.blit(rotated, rect.topleft)

def main():
    clock = pygame.time.Clock()
    car = Car(WIDTH//2, HEIGHT//2)
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        car.update()
        win.fill((30, 30, 30))
        car.draw(win)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
