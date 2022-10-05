from typing import List
import pygame
from sprites.player import Player
from debug import debugger

class Hitbox(pygame.sprite.Sprite):
    def __init__(
        self, 
        side_lg: int,
        side_sm: int, 
        color: any,
        player: Player,
        groups: List[pygame.sprite.Group], 
        enemys_group: pygame.sprite.Group
    ) -> None:
        super().__init__(groups)
        self.player = player
        self.enemys_group = enemys_group
        if "up" in self.player.status or "down" in player.status: hitbox = (side_lg, side_sm)
        elif "left" in self.player.status or "right" in player.status: hitbox = (side_sm, side_lg)
        self.image = pygame.Surface(hitbox)
        self.image.fill(color)
        self.image.set_alpha(0)
        if debugger.active: self.image.set_alpha(100)
        self.rect = self.image.get_rect(center = self.player.rect.center)  

    def handle_hits(self) -> None:
        pass

    def set_position(self) -> None:
        if "up" in self.player.status:
            self.rect = self.image.get_rect(midtop = self.player.rect.center - pygame.math.Vector2(0, 30))
        elif "down" in self.player.status:
            self.rect = self.image.get_rect(midbottom = self.player.rect.center - pygame.math.Vector2(0, -30))
        elif "left" in self.player.status:
            self.rect = self.image.get_rect(midleft = self.player.rect.center - pygame.math.Vector2(30, 0))
        elif "right" in self.player.status:
            self.rect = self.image.get_rect(midright = self.player.rect.center - pygame.math.Vector2(-30, 0))

    def update(self):
        self.handle_hits()
        self.set_position()

class Attack(Hitbox):
    def __init__(self, player: Player, groups: List[pygame.sprite.Group], enemys_group: pygame.sprite.Group) -> None:
        super().__init__(45, 25, "Red", player, groups, enemys_group)

    def handle_hits(self) -> None:
        if self.player.is_attacking:
            for enemy in self.enemys_group:
                if enemy.rect.colliderect(self.rect):
                    if not enemy.attacked:
                        enemy.attacked_time = pygame.time.get_ticks()
                        enemy.attacked = True
                        enemy.frame_index = 0
                        enemy.current_health -= self.player.stats.damage
        else: 
            self.kill()

class Protection(Hitbox):
    def __init__(self, player: Player, groups: List[pygame.sprite.Group], enemys_group: pygame.sprite.Group) -> None:
        super().__init__(20, 10, "Blue", player, groups, enemys_group)
        self.player.protection_hitbox_created = True

    def handle_hits(self) -> None:
        for enemy in self.enemys_group:
            if self.player.is_shielded:
                if enemy.rect.colliderect(self.rect):
                    enemy.attacks_protected_by_user = True
                else:
                    enemy.attacks_protected_by_user = False
            else:
                enemy.attacks_protected_by_user = False
                self.player.protection_hitbox_created = False
                self.kill()