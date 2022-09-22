from typing import List, Tuple
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int], 
        groups: List[pygame.sprite.Group],
        obstacle_sprites_group: pygame.sprite.Group
    ) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("assets/player/elf_m_idle_anim_f0.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-6, -12)
        self.obstacle_sprites_group = obstacle_sprites_group
        self.speed: int = 3
        self.frame_index: int = 0
        self.direction = pygame.math.Vector2()
        self.heading: str = "right"

    def animate(self):
        static_frames = [
            pygame.image.load("assets/player/elf_m_idle_anim_f0.png").convert_alpha(),
            pygame.image.load("assets/player/elf_m_idle_anim_f1.png").convert_alpha()
        ]

        run_frames: List[pygame.Surface] = [
            pygame.image.load("assets/player/elf_m_run_anim_f0.png").convert_alpha(),
            pygame.image.load("assets/player/elf_m_run_anim_f1.png").convert_alpha(),
            pygame.image.load("assets/player/elf_m_run_anim_f2.png").convert_alpha(),
            pygame.image.load("assets/player/elf_m_run_anim_f3.png").convert_alpha()
        ]

        if self.direction.x == 0 and self.direction.y == 0: # Static
            self.frame_index += 0.1
            if self.frame_index >= len(static_frames): self.frame_index = 0
            image = pygame.transform.scale2x(static_frames[int(self.frame_index)])
            if self.heading == "left": image = pygame.transform.flip(image, True, False)
            self.image = image
        else:
            self.frame_index += 0.3
            if self.frame_index >= len(run_frames): self.frame_index = 0
            image= pygame.transform.scale2x(run_frames[int(self.frame_index)])
            if self.heading == "left": image = pygame.transform.flip(image, True, False)
            self.image = image

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.heading = "left"
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.heading = "right"
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed: int) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.handle_collitions("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.handle_collitions("vertical")
        self.rect.center = self.hitbox.center

    def handle_collitions(self, direction: str) -> None:
        if direction == "horizontal":
            for sprite in self.obstacle_sprites_group:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # Right ->
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # Left <-
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites_group:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # Down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # Top
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self) -> None:
        self.handle_input()
        self.animate()
        self.move(self.speed)