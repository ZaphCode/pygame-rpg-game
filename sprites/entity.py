import pygame
from typing import List

class Entity(pygame.sprite.Sprite):
    def __init__(
    self,
    groups: List[pygame.sprite.Group], 
    obstacle_sprites_group: pygame.sprite.Group
) -> None:
        super().__init__(groups)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites_group = obstacle_sprites_group

    def move(self, speed: int) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.handle_collisions("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.handle_collisions("vertical")
        self.rect.center = self.hitbox.center

    def handle_collisions(self, direction: str) -> None:
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