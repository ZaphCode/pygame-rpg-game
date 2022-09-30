import pygame

class ButtonGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def _draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, dest=sprite.rect)
            self.display_surface.blit(sprite.text, dest=sprite.text_rect)