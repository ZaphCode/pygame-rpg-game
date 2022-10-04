import pygame
from sprites.chest import Chest
from sprites.enemy import Enemy
from sprites.item import Item
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
        self.item_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame("./assets/level/main_level.tmx")
        self.build_map()

    def build_map(self) -> None:
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                if layer.name == "Flags":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("flag", (x * TILESIZE, y * TILESIZE), 2, 0.1, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "Torchs":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("torch", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "TorchsRight":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("side_torch", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites], True)
                elif layer.name == "TorchsLeft":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("side_torch", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "CandlesticksLG":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("candlestick_lg", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites])
                elif layer.name == "CandlesticksSM":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("candlestick_sm", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites])
                elif layer.name == "Arrows":
                    for x, y, surf in layer.tiles():
                        AnimatedDeco("arrow", (x * TILESIZE, y * TILESIZE), 2, 0.2, [self.visible_y_sorteed_camera_sprites])
                elif layer.name == "Walls" or layer.name == "Doors":
                    for x, y, surf in layer.tiles():
                        Tile(surf, (x * TILESIZE, y * TILESIZE), [self.visible_y_sorteed_camera_sprites, self.obstacle_sprites], 0, 8)
                else:
                    for x, y, surf in layer.tiles():
                        Tile(surf, (x * TILESIZE, y * TILESIZE), [self.visible_camera_sprites])
        for obj in self.tmx_data.objects:
            if obj.name == "chest":
                Chest(obj.loot, (obj.x * 2, obj.y * 2), [self.visible_y_sorteed_camera_sprites, self.item_sprites, self.obstacle_sprites])
            else:
                Item(obj.name, (obj.x * 2, obj.y * 2), [self.visible_y_sorteed_camera_sprites, self.item_sprites])
        self.player = Player((162, 1408), [self.visible_y_sorteed_camera_sprites], self.obstacle_sprites, self.item_sprites, self.create_attack)
        Enemy("bat", (292, 1420), [self.visible_y_sorteed_camera_sprites], self.obstacle_sprites, self.player)

    def create_attack(self) -> None:
        Attack(self.player, self.visible_y_sorteed_camera_sprites) 

    def run(self) -> None:
        self.visible_y_sorteed_camera_sprites.update()
        self.visible_camera_sprites.update()
        self.visible_camera_sprites._draw(self.player)
        self.visible_y_sorteed_camera_sprites._draw(self.player)
        debugger.show(self.player.direction, 40)
        debugger.show(self.player.rect.center, 70)
        debugger.show(self.player.status, 100)
        debugger.show(f"protecting: {self.player.is_shielded}", 130)
        debugger.show(f"silver_key: {self.player.has_silver_key}", 160)
        debugger.show(f"crystals: {self.player.crystals}", 190)
        debugger.show(f"interacting: {self.player.is_object_interacting}", 220)
        