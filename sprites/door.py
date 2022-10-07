from typing import List
import pygame
from pygame.transform import scale
from sprites.player import Player

class Door(pygame.sprite.Sprite):
    def __init__(
        self, 
        door_type: str, 
        key_required: str,
        position, 
        player: Player,
        groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(f"assets/doors/{door_type}.png").convert_alpha()
        self.image = scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))
        self.rect = self.image.get_rect(topleft = position)
        self.key_required = key_required
        self.player = player
        self.opened: bool = False
        self.hitbox = self.rect.inflate(-20, 0)
        self.interact_ratio = self.rect.inflate(40, 40)

    def check_interact_ratio(self) -> None:
        if self.interact_ratio.colliderect(self.player.hitbox):
            keys = pygame.key.get_pressed()
            self.player.object_interacting_time = pygame.time.get_ticks()
            self.player.is_object_interacting = True
            if keys[pygame.K_SPACE]:
                if self.key_required == "silver_key":
                    if self.player.has_silver_key:
                        self.kill()
                        self.player.has_silver_key = False
                        return
                elif self.key_required == "golden_key":
                    if self.player.has_golden_key:
                        self.kill()
                        self.player.has_silver_key = False
                        return



    def update(self) -> None:
        self.check_interact_ratio()
        

