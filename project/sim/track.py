import pygame

class Track:
    def __init__(self, track_path):
        raw_image = pygame.image.load(track_path)
        self.image = raw_image.convert()
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size

        # Máscara da pista válida (parte branca)
        self.valid_mask = pygame.mask.from_threshold(
            self.image, (255, 255, 255), (10, 10, 10)
        )

        # Alias para facilitar integração com o carro
        self.mask = self.valid_mask

        # Máscara da pista inválida = pixels que NÃO são brancos
        self.invalid_mask = pygame.Mask((self.width, self.height))
        self.invalid_mask.fill()  # tudo preenchido
        self.invalid_mask.erase(self.valid_mask, (0, 0))  # remove parte válida

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def check_collision(self, car):
        # Deslocamento entre carro e pista
        offset = (car.rect.x - self.rect.x, car.rect.y - self.rect.y)

        # Agora testamos contra a área INVÁLIDA
        overlap = self.invalid_mask.overlap(car.mask, offset)

        return overlap is not None
