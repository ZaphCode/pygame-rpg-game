from typing import List, Tuple
import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, 
        surf: pygame.Surface,
        position: Tuple[int, int], 
        groups: List[pygame.sprite.Group],
        hitbo_x: int = 0,
        hitbo_y: int = 0,
    ) -> None:
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(hitbo_x, hitbo_y)