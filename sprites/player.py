from typing import List, Tuple
import pygame
from lib.files import import_folder
from pygame.transform import scale, flip
from pygame.image import load
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int], 
        groups: List[pygame.sprite.Group],
        obstacle_sprites_group: pygame.sprite.Group,
        create_attack,
        disabled: bool = False
    ) -> None:
        super().__init__(groups)
        self.image = scale(load("assets/player/down/char_run_down_1.png").convert_alpha(), (38, 32))
        self.rect = self.image.get_rect(midbottom = position)
        self.hitbox = self.rect.inflate(-4, -4)
        self.obstacle_sprites_group = obstacle_sprites_group
        self.create_attack = create_attack
        self.disabled = disabled
        # Movement
        self.speed: int = 3
        self.direction = pygame.math.Vector2()
        # Animation
        self.frame_index: int = 0
        self.animations: dict = {
            "up": [], "down": [], "right": [], "left": [],
            "up_idle": [], "down_idle": [], "right_idle": [], "left_idle": [],
            "up_attack": [], "down_attack": [], "right_attack": [], "left_attack": [],
        }
        self.status: str = "down"
        self.load_animations()
        # Attacking
        self.is_attacking: bool = False
        self.attack_available: bool = True
        self.attacking_cooldown: int = 400
        self.attack_again_cooldown: int = 1000
        self.attack_time = None
        # Shield
        self.is_proteting: bool = False
        self.protection_time: None
        self.protection_cooldown: int = 5000

    def load_animations(self) -> None:
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"assets/player/{animation}")

    def animate(self) -> None:
        current_animation: List[pygame.Surface] = self.animations[self.status]
        self.frame_index += 0.2
        if self.frame_index >= len(current_animation): self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)
        if self.is_attacking:
            if self.status == "up_attack":
                pass

    def handle_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.is_attacking:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.status = "up"
                self.direction.y = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.status = "down"
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.status = "left"
                self.direction.x = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.status = "right"
                self.direction.x = 1
            else:
                self.direction.x = 0    
        
        if keys[pygame.K_SPACE] and self.attack_available:
            self.is_attacking = True
            self.frame_index = 0
            self.attack_available = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            print("attack")
        
        if keys[pygame.K_LCTRL] and not self.is_attacking:
            self.is_proteting = True
            self.protection_time = pygame.time.get_ticks()

    def move(self, speed: int) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.handle_collitions("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.handle_collitions("vertical")
        self.rect.center = self.hitbox.center

    def handle_status(self):
        if self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else: 
                    self.status += "_attack"
        else: 
            self.status = self.status.split("_")[0]

        if self.direction.x == 0 and self.direction.y == 0: #idle
            if not "idle" in self.status and not "attack" in self.status: 
                self.status += "_idle"
        
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
    
    def cooldowns(self) -> None:
        current_time = pygame.time.get_ticks()

        if self.is_proteting:
            if current_time - self.protection_time >= self.protection_cooldown:
                self.is_proteting = False

        if self.is_attacking:
            if current_time - self.attack_time >= self.attacking_cooldown:
                self.is_attacking = False

        if not self.attack_available:
            if current_time - self.attack_time >= self.attack_again_cooldown:
                self.attack_available = True

    def update(self) -> None:   
        if not self.disabled:
            self.handle_inputs()
            self.handle_status()
            self.cooldowns() 
            self.animate()
            self.move(self.speed)
        else:
            self.animate()