import pygame
from lib.ui import UI
from settings import *
from groups.buttons import ButtonGroup
from sprites.button import Button
from sprites.static import StaticSprite

class Modal(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)
        
    def create_ui(self) -> None:
        StaticSprite("assets/ui/ui-modal-4.png", (WIDTH / 2, 240), [self.images_group], (400, 300))
        Button("lg", "Restart", (WIDTH/2, 200), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Exit", (WIDTH/2, 270), [self.button_group], lambda: self.set_status_fn("exit"))
    
  