from displays.ui import UI
from sprites.font import Font
from settings import *
from sprites.button import Button
from sprites.static import StaticSprite

class Pause(UI):
    def __init__(self, set_status_fn) -> None:
        super().__init__(set_status_fn)
        
    def create_ui(self) -> None:
        Font("Pause", 70, "White", (WIDTH/2, 140), [self.images_group], is_title=True)
        StaticSprite("assets/ui/ui-square.png", (WIDTH/2, 280), [self.images_group], (240, 200))
        Button("lg", "Restart", (WIDTH/2, 245), [self.button_group], lambda: self.set_status_fn("playing"))
        Button("lg", "Exit", (WIDTH/2, 315), [self.button_group], lambda: self.set_status_fn("exit"))
    
    