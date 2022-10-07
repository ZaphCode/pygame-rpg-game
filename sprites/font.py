import pygame
from settings import MAIN_FONT_SRC, TITLE_FONT_SRC

class Font(pygame.sprite.Sprite):
    def __init__(self, text: str, size: int, color, pos, groups, is_title = False) -> None:
        super().__init__(groups)
        font_src = MAIN_FONT_SRC
        if is_title: font_src = TITLE_FONT_SRC
        pixel_font = pygame.font.Font(font_src, size)
        self.image = pixel_font.render(text, False, color)
        self.rect = self.image.get_rect(center = pos)

    