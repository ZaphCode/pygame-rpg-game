from lib.ui import UI
from settings import *
from sprites.button import Button
from sprites.font import Font
from sprites.player import Player

class Menu(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)

    def create_ui(self) -> None:
        Player((WIDTH/2, 200), [self.images_group], None, None, True, 4)
        Font("The Legends of Zelda", 35, "#FFE156",  (WIDTH/2, 60), [self.images_group])
        Font("UABCS version", 28, "#FF3C3C",  (WIDTH/2, 110), [self.images_group])
        Button("lg", "Start", (WIDTH/2, 300 - 30), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Settings", (WIDTH/2, 370 -30), [self.button_group])
        Button("lg", "Exit", (WIDTH/2, 440 -30), [self.button_group], lambda: self.set_status_fn("exit"))
