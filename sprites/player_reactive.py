import pygame
from settings import MAIN_FONT_SRC
from sprites.player import Player
from pygame.transform import scale

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
        self.image = pygame.image.load("assets/ui/health_bar.png").convert_alpha()
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

    

