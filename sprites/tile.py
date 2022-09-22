from typing import List, Tuple
import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int], 
        groups: List[pygame.sprite.Group]
    ) -> None:
        super().__init__(groups)
        self.image = pygame.transform.scale2x(pygame.image.load("assets/floor_3.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -10)