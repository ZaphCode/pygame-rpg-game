from typing import List
import pygame
from sprites.player import Player
from lib.files import import_folder

class Item(pygame.sprite.Sprite):
    def __init__(
        self, 
        type: str, position, 
        groups: List[pygame.sprite.Group], 
        scale: float = 2, 
        animation_speed: float = 0.1,
        kill_on_touch: bool = True
    ) -> None:
        super().__init__(groups)
        self.type = type
        if self.type in ["crystal", "chest"]: 
            self.has_touched_animation = True
        else: 
            self.has_touched_animation = False
        self.default_frames = import_folder(f"assets/{type}/default", scale)
        if self.has_touched_animation: 
            self.touched_frames = import_folder(f"assets/{type}/touched", scale)
        self.animation_speed = animation_speed
        self.kill_on_touch = kill_on_touch
        self.touched: bool = False
        self.frame_index = 0
        self.static = False
        self.image = self.default_frames[0]
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, 0)
        self.interact_ratio = self.rect.inflate(0, 0)
        
    def on_touched(self, player: Player):
        if not self.touched and not self.static:
            if self.type == "crystal":
                player.crystals += 1
            elif self.type == "golden_key":
                player.has_golden_key = True
            elif self.type == "silver_key":
                player.has_silver_key = True
            elif self.type == "speed_potion":
                player.stats.speed = 5
            self.frame_index = 0
            self.animation_speed = 0.2
            self.touched = True

    def animate(self) -> None:
        if not self.touched:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.default_frames): self.frame_index = 0
            self.image = self.default_frames[int(self.frame_index)]  
        else:
            if self.has_touched_animation:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.touched_frames): 
                    if self.kill_on_touch:
                        self.kill()
                    else:
                        self.static = True
                    return
                self.image = self.touched_frames[int(self.frame_index)]  
            else:
                if self.kill_on_touch:
                    self.kill()
    
    def update(self) -> None:
        if not self.static:
            self.animate()
        