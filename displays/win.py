from displays.ui import UI
from sprites.static import StaticSprite
from sprites.player import Player
from sprites.font import Font
from sprites.button import Button
from settings import *

class Win(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)

    def create_ui(self) -> None:
        StaticSprite("assets/ui/bg-main.jpg", (WIDTH/2, HEIGHT/2), [self.images_group], (WIDTH, HEIGHT))
        Font("You Win!", 55, "White",  (WIDTH/2, 130), [self.images_group], is_title=True)
        StaticSprite("assets/ui/ui-square.png", (WIDTH/2, 280), [self.images_group], (240, 200))
        Button("lg", "Restart", (WIDTH/2, 245), [self.button_group], lambda: self.set_status_fn("restart"))
        Button("lg", "Exit", (WIDTH/2, 315), [self.button_group], lambda: self.set_status_fn("exit"))