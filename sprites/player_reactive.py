import pygame
from settings import MAIN_FONT_SRC
from sprites.player import Player
from pygame.transform import scale
from pygame.image import load


class PlayerReactive(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        self.player = player

    def handle_change(self) -> None:
        pass

    def update(self) -> None:
        self.handle_change()

class HealthBar(PlayerReactive):
    def __init__(self, position, player: Player, groups) -> None:
        super().__init__(player, groups)
        self.image = load("assets/ui/health_bar.png").convert_alpha()
        self.rect = self.image.get_rect(midleft = position)

    def handle_change(self) -> None:
        max_width = 130
        proportion = (self.player.current_health * max_width / self.player.stats.health)
        if proportion < 0 or self.player.current_health <= 0:
            self.kill()
            return
        self.image = scale(self.image, (proportion, 8))

class CrystalCount(PlayerReactive):
    def __init__(self, position, player: Player, groups) -> None:
        super().__init__(player, groups)
        self.pixel_font = pygame.font.Font(MAIN_FONT_SRC, 15)
        self.image = self.pixel_font.render(f"{self.player.crystals}", False, "White")
        self.rect = self.image.get_rect(topright = position)
        self.moved = False

    def handle_change(self) -> None:
        self.image = self.pixel_font.render(f"{self.player.crystals}", False, "White")
        if self.player.crystals >= 10 and not self.moved:
            self.rect.x -= 7
            self.moved = True

class KeySlot(PlayerReactive):
    def __init__(self, type: str, position, player: Player, groups) -> None:
        super().__init__(player, groups)
        self.scale = (26, 26)
        self.image = scale(load("assets/ui/key_not_picked.png").convert_alpha(), self.scale)
        self.type = type
        self.rect = self.image.get_rect(topleft = position)
        self.has_changed = False

    def handle_change(self) -> None:
        if not self.has_changed:
            if self.type == "silver_key" and self.player.has_silver_key:
                self.image = scale(load("assets/silver_key/static.png").convert_alpha(), self.scale)
                self.has_changed = True
            elif self.type == "golden_key" and self.player.has_golden_key:
                self.image = scale(load("assets/golden_key/static.png").convert_alpha(), self.scale)
                self.has_changed = True


    

