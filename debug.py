import pygame
from settings import DEBUG_FONT_COLOR
pygame.init()
font = pygame.font.Font(None, 30)

class Debugger:
    def __init__(self) -> None:
        self.active = False

    def show(self, info,y = 10, x = 10):
        if self.active:
            display_surface = pygame.display.get_surface()
            debug_text = font.render(str(info),True, DEBUG_FONT_COLOR)
            debug_bg = pygame.Surface((debug_text.get_width(), debug_text.get_height()))
            debug_bg.set_alpha(100)
            debug_rect = debug_text.get_rect(topleft = (x,y))
            display_surface.blit(debug_bg,debug_rect)
            display_surface.blit(debug_text,debug_rect)

debugger = Debugger()