import pygame

class Track:
    def __init__(self, track_path):
        # Load image
        self.image = pygame.image.load(track_path).convert()
        self.rect = self.image.get_rect()

        # Create mask for collision detection
        self.mask = pygame.mask.from_threshold(self.image, (255, 255, 255), (1, 1, 1))  # detecta área branca como pista

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def check_collision(self, car_rect):
        offset = (car_rect.x - self.rect.x, car_rect.y - self.rect.y)
        overlap = self.mask.overlap_area(pygame.mask.Mask(car_rect.size, True), offset)
        return overlap == 0  # retorna True se saiu da pista
