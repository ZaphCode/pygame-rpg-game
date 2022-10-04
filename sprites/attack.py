from typing import List
import pygame
from sprites.player import Player
from debug import debugger

class Attack(pygame.sprite.Sprite):
    def __init__(
        self, 
        player: Player, 
        groups: List[pygame.sprite.Group], 
        enemys_group: pygame.sprite.Group
    ) -> None:
        super().__init__(groups)
        self.player = player
        self.enemys_group = enemys_group
        if "up" in self.player.status or "down" in player.status: hitbox = (45, 25)
        elif "left" in self.player.status or "right" in player.status: hitbox = (25, 45)
        self.image = pygame.Surface(hitbox)
        self.image.fill("Red")
        self.image.set_alpha(0)
        if debugger.active: self.image.set_alpha(100)
        self.rect = self.image.get_rect(center = self.player.rect.center)    

    def handle_hits(self) -> None:
        for enemy in self.enemys_group:
            if enemy.rect.colliderect(self.rect):
                if not enemy.attacked:
                    enemy.attacked_time = pygame.time.get_ticks()
                    enemy.attacked = True
                    enemy.frame_index = 0
                    enemy.current_health -= self.player.stats.damage

    def update(self):
        self.handle_hits()
        if "up" in self.player.status:
            self.rect = self.image.get_rect(midtop = self.player.rect.center - pygame.math.Vector2(0, 30))
        elif "down" in self.player.status:
            self.rect = self.image.get_rect(midbottom = self.player.rect.center - pygame.math.Vector2(0, -30))
        elif "left" in self.player.status:
            self.rect = self.image.get_rect(midleft = self.player.rect.center - pygame.math.Vector2(30, 0))
        elif "right" in self.player.status:
            self.rect = self.image.get_rect(midright = self.player.rect.center - pygame.math.Vector2(-30, 0))
        if not self.player.is_attacking:
            self.kill()