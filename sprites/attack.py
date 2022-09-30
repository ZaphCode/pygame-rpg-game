import pygame
from sprites.player import Player
from debug import debugger

class Attack(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        self.frames= []
        self.player = player
        hitbox = ()

        if "up" in self.player.status or "down" in player.status: hitbox = (45, 25)
        elif "left" in self.player.status or "right" in player.status: hitbox = (25, 45)

        self.image = pygame.Surface(hitbox)
        self.image.fill("Red")
        self.image.set_alpha(0)
        if debugger.active: self.image.set_alpha(100)

        if "up" in player.status:
            self.rect = self.image.get_rect(midtop = self.player.rect.center - pygame.math.Vector2(0, 30))
        elif "down" in player.status:
            self.rect = self.image.get_rect(midbottom = self.player.rect.center - pygame.math.Vector2(0, -30))
        elif "left" in player.status:
            self.rect = self.image.get_rect(midleft = self.player.rect.center - pygame.math.Vector2(30, 0))
        elif "right" in player.status:
            self.rect = self.image.get_rect(midright = self.player.rect.center - pygame.math.Vector2(-30, 0))    

    def update(self):
        if not self.player.is_attacking:
            self.kill()