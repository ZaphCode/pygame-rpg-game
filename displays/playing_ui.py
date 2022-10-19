from displays.ui import UI
from sprites.item import Item
from sprites.player import Player
from sprites.player_reactive import CrystalCount, HealthBar, KeySlot
from sprites.static import StaticSprite

class PlayingUI(UI):
    def __init__(self, set_status_fn, player: Player) -> None:
        self.player = player
        super().__init__(set_status_fn)
    
    def create_ui(self) -> None:
        StaticSprite("assets/ui/health_bar_border.png", (50 + 30, 40), [self.images_group],  size=(140, 19.5), center=False)
        StaticSprite("assets/ui/ui-bar.png", (80.5, 62), [self.images_group],  size=(80, 28), center=False)
        HealthBar((84, 38), self.player, [self.images_group])
        StaticSprite("assets/ui/ui-square.png", (30, 55), [self.images_group], size=(50, 50), center=False)
        Item("crystal", (38, 39), [self.images_group], scale=2.3)
        KeySlot("silver_key", (88, 49), self.player, [self.images_group])
        KeySlot("golden_key", (116, 49), self.player, [self.images_group])
        CrystalCount((75, 60), self.player, [self.images_group])