import pygame
from settings import *
from groups.buttons import ButtonGroup
from sprites.button import Button
from sprites.static import StaticSprite

class Modal:
    def __init__(self, set_status_fn) -> None:
        self.display_surface = pygame.display.get_surface()
        self.button_group = ButtonGroup()
        self.images_group = pygame.sprite.Group()
        self.set_status_fn = set_status_fn
        self.create_ui()
        
    def create_ui(self) -> None:
        StaticSprite("assets/ui/ui-modal-4.png", (WIDTH / 2, 240), [self.images_group], (400, 300))
        Button("lg", "Restart", (WIDTH/2, 200), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Exit", (WIDTH/2, 270), [self.button_group], lambda: self.set_status_fn("exit"))
        

    
    def run(self) -> None:
        self.button_group.update()
        self.images_group.update()
        self.images_group.draw(self.display_surface)
        self.button_group._draw()