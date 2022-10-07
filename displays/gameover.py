from sprites.button import Button
from displays.ui import UI
from sprites.font import Font
from sprites.player import Player
from sprites.static import StaticSprite
from settings import *

class Gameover(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)
        self.display_surface.fill("#262b44")

    def create_ui(self) -> None:
        StaticSprite("assets/ui/bg-main.jpg", (WIDTH/2, HEIGHT/2), [self.images_group], (WIDTH, HEIGHT))
        StaticSprite("assets/ui/ui-square.png", (WIDTH/2, HEIGHT/2 + 45), [self.images_group], (255, 290))
        Player((WIDTH/2, 219), [self.images_group], disabled=True, scale=4.5, default_status="down_hit")
        Font("Gameover", 60, "White",  (WIDTH/2, 90), [self.images_group], is_title=True)
        Button("lg", "Restart", (WIDTH/2, 290), [self.button_group], lambda: self.set_status_fn("restart"))
        Button("lg", "Exit", (WIDTH/2, 360), [self.button_group], lambda: self.set_status_fn("exit"))