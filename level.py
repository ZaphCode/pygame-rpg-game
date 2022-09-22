import pygame
from settings import *
from sprites.camera_group import CameraGroup
from sprites.tile import Tile
from sprites.player import Player
from debug import debugger

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.build_map()

    def build_map(self) -> None:
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self) -> None:
        self.visible_sprites.update()
        self.visible_sprites._draw(self.player)
        debugger.show(self.player.direction, 40, 10)
        