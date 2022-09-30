import pygame

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, src: str, position, groups, size = None) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(src).convert_alpha()
        if size:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center = position)