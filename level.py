import pygame
from settings import *
from groups.camera import CameraGroup, YSortedCameraGroup
from sprites.tile import Tile
from sprites.player import Player
from debug import debugger
from sprites.animated_deco import AnimatedDeco
from pytmx.util_pygame import load_pygame

from sprites.attack import Attack

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_camera_sprites = CameraGroup()
        self.visible_y_sorteed_camera_sprites = YSortedCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame("./assets/level/main_level.tmx")
        self.build_map()

    def build_map(self) -> None:
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                if layer.name == "Coins":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("coin", (pos_x, pos_y), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "Flags":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("flag", (pos_x, pos_y), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "Torchs":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("torch", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "TorchsRight":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("side_torch", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites], True)
                elif layer.name == "TorchsLeft":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("side_torch", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "CandlesticksLG":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("candlestick_lg", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites])
                elif layer.name == "CandlesticksSM":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("candlestick_sm", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites])
                elif layer.name == "Arrows":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        AnimatedDeco("arrow", (pos_x, pos_y), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "Walls" or layer.name == "HardDeco":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        Tile(surf, (pos_x, pos_y), [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites], 0, 8)
                elif layer.name == "WallsDeco":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        Tile(surf, (pos_x, pos_y), [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "WallsTop":
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        Tile(surf, (pos_x, pos_y), [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites], 0, -30)
                else:
                    for x, y, surf in layer.tiles():
                        pos_x = x * 32
                        pos_y = y * 32
                        Tile(surf, (pos_x, pos_y), [self.visible_camera_sprites])
        #Tile(pygame.Surface((40, 40)), (32 * 7, 32 * 12), [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites], hitbo_x=-10, hitbo_y=10)
        self.player = Player((162, 1408), [self.visible_y_sorteed_camera_sprites], self.obstacle_sprites, self.create_attack)
        # AnimatedDeco("flag", (110, 1280), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("torch", (150, 1280), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("candlestick_sm", (170, 1310), 2.5, 0.2, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("coin", (170, 1370), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("side_torch", (65, 1370), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("golden_key", (80, 1400), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
        # AnimatedDeco("red_potion", (160, 1400), 2, 0.1, [self.visible_y_sorteed_camera_sprites])

    def create_attack(self) -> None:
        Attack(self.player, self.visible_y_sorteed_camera_sprites) 

    def run(self) -> None:
        self.visible_y_sorteed_camera_sprites.update()
        self.visible_camera_sprites.update()
        self.visible_camera_sprites._draw(self.player)
        self.visible_y_sorteed_camera_sprites._draw(self.player)
        debugger.show(self.player.direction, 40, 10)
        debugger.show(self.player.rect.center, 70, 10)
        debugger.show(self.player.status, 100, 10)
        debugger.show(f"protecting: {self.player.is_shielded}", 130, 10)
        debugger.show(f"lh: {self.player.last_heanding}", 160, 10)
        