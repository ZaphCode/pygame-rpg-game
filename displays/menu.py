from displays.ui import UI
from settings import *
from sprites.button import Button
from sprites.font import Font
from sprites.player import Player
from sprites.static import StaticSprite

class Menu(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)
        self.display_surface.fill("#262b44")

    def create_ui(self) -> None:
        StaticSprite("assets/ui/bg-main.jpg", (WIDTH/2, HEIGHT/2), [self.images_group], (WIDTH, HEIGHT))
        StaticSprite("assets/ui/ui-square.png", (WIDTH/2, HEIGHT/2 + 45), [self.images_group], (255, 290))
        Player((WIDTH/2, 214), [self.images_group], disabled=True, scale=4.5)
        Font("The Legends of Zelda", 55, "White",  (WIDTH/2, 60), [self.images_group], is_title=True)
        Font("uabcs version", 24, "Gray",  (WIDTH/2, 115), [self.images_group])
        Button("lg", "Start", (WIDTH/2, 290), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Exit", (WIDTH/2, 360), [self.button_group], lambda: self.set_status_fn("exit"))
