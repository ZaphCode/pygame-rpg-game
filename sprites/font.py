import pygame
from settings import MAIN_FONT_SRC

class Font(pygame.sprite.Sprite):
    def __init__(self, text: str, size: int, color, pos, groups) -> None:
        super().__init__(groups)
        pixel_font = pygame.font.Font(MAIN_FONT_SRC, size)
        self.image = pixel_font.render(text, False, color)
        self.rect = self.image.get_rect(center = pos)
