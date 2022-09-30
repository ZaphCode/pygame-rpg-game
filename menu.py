import pygame
from settings import *
from groups.buttons import ButtonGroup
from sprites.button import Button
from sprites.demon_chort import DemonChort
from sprites.font import Font
from sprites.player import Player

class Menu():
    def __init__(self, set_status_fn) -> None:
        self.display_surface = pygame.display.get_surface()
        self.button_group = ButtonGroup()
        self.images_group = pygame.sprite.Group()
        self.set_status_fn = set_status_fn
        self.create_ui()

    def create_ui(self) -> None:
        #Player((WIDTH/2 - 80, 140), [self.images_group], None, None, True)
        #DemonChort((WIDTH/2 + 20, 140), [self.images_group])
        Font("The Legends of Zelda", 35, "#FFE156",  (WIDTH/2, 60), [self.images_group])
        Font("UABCS version", 28, "#FF3C3C",  (WIDTH/2, 110), [self.images_group])
        Button("lg", "Start", (WIDTH/2, 300 - 30), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Settings", (WIDTH/2, 370 -30), [self.button_group])
        Button("lg", "Exit", (WIDTH/2, 440 -30), [self.button_group], lambda: self.set_status_fn("exit"))

    def run(self) -> None:
        self.button_group.update()
        self.images_group.update()
        self.button_group._draw()
        self.images_group.draw(self.display_surface)
