import pygame
from groups.buttons import ButtonGroup

class UI:
    def __init__(self, set_status_fn) -> None:
        self.display_surface = pygame.display.get_surface()
        self.set_status_fn = set_status_fn
        self.button_group = ButtonGroup()
        self.images_group = pygame.sprite.Group()
        self.create_ui()
    
    def create_ui(self) -> None:
        pass

    def render(self) -> None:
        self.button_group.update()
        self.images_group.update()
        self.images_group.draw(self.display_surface)
        self.button_group._draw()