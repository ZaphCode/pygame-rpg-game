from typing import List
import pygame
from lib.files import import_folder



class AnimatedDeco(pygame.sprite.Sprite):
    def __init__(
        self, 
        src: str, 
        position,
        scale: int, 
        animate_speed: float,
        groups: List[pygame.sprite.Group],
        flip: bool = False
    ) -> None:
        super().__init__(groups)
        self.frames = import_folder(f"assets/decoration/{src}", scale, flip)
        self.frame_index: int = 0
        self.animation_speed = animate_speed
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-20, -20)

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        self.animate()
