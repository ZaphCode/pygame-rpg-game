from typing import List, Tuple
import pygame
from lib.files import import_folder
from pygame.transform import scale as _scale
from pygame.image import load
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int], 
        groups: List[pygame.sprite.Group],
        obstacle_sprites_group: pygame.sprite.Group,
        items_sprite_group: pygame.sprite.Group,
        create_attack,
        disabled: bool = False,
        scale: float = 2.8
    ) -> None:
        super().__init__(groups)
        self.image = _scale(load("assets/player/down/char_run_down_1.png").convert_alpha(), (38, 32))
        self.rect = self.image.get_rect(midbottom = position)
        self.hitbox = self.rect.inflate(-6, -16)
        self.obstacle_sprites_group = obstacle_sprites_group
        self.items_sprite_group = items_sprite_group
        self.create_attack = create_attack
        self.disabled = disabled
        # Movement
        self.max_speed: int = PLAYER_SPEED
        self.speed: int = PLAYER_SPEED
        self.direction = pygame.math.Vector2()
        # Animation
        self.frame_index: int = 0
        self.animations: dict = {
            "up": [], "down": [], "right": [], "left": [],
            "up_idle": [], "down_idle": [], "right_idle": [], "left_idle": [],
            "up_attack": [], "down_attack": [], "right_attack": [], "left_attack": [],
            "up_shielded": [], "down_shielded": [], "right_shielded": [], "left_shielded": [],

        }
        self.status: str = "down_idle"
        self.last_heanding: str = "down"
        self.load_animations(scale)
        # Attacking
        self.is_attacking: bool = False
        self.attack_available: bool = False
        self.attacking_cooldown: int = 400
        self.attack_again_cooldown: int = 1000
        self.attack_time = pygame.time.get_ticks()
        # Shield
        self.is_shielded: bool = False
        self.shield_available: bool = True
        self.shield_time = None
        self.shield_again_cooldown: int = 400
        # Intems
        self.crystals: int = 0
        self.has_silver_key: bool = False
        self.has_golden_key: bool = False
        self.is_object_interacting = False
        self.object_interacting_time = None

    def load_animations(self, scale) -> None:
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"assets/player/{animation}", scale)

    def animate(self) -> None:
        current_animation: List[pygame.Surface] = self.animations[self.status]
        self.frame_index += 0.2
        if self.frame_index >= len(current_animation): self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def handle_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.is_attacking and not self.is_shielded:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.status, self.last_heanding = "up", "up"
                self.direction.y = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.status, self.last_heanding = "down", "down"
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.status, self.last_heanding = "left", "left"
                self.direction.x = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.status, self.last_heanding = "right", "right"
                self.direction.x = 1
            else:
                self.direction.x = 0    
        
        if keys[pygame.K_SPACE] and self.attack_available and not self.is_shielded and not self.is_object_interacting:
            self.is_attacking = True
            self.frame_index = 0
            self.attack_available = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        if keys[pygame.K_LCTRL]:
            if not self.is_attacking and self.shield_available:
                self.is_shielded = True
                self.shield_available = False
                self.shield_time = pygame.time.get_ticks()
        else:
            self.is_shielded = False
            
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
            self.speed = self.max_speed / 2
            if not "attack" in self.status:
                self.status = self.last_heanding + "_attack"
        else: 
            self.speed = self.max_speed 
            self.status = self.last_heanding

        if self.is_shielded: 
            self.direction.x = 0
            self.direction.y = 0
            if not "shielded" in self.status:
                self.status = self.last_heanding + "_shielded"

        if self.direction.x == 0 and self.direction.y == 0: #idle
            if not "idle" in self.status and not self.is_shielded and not self.is_attacking: 
                self.status = self.last_heanding + "_idle"
             
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

        if self.is_attacking:
            if current_time - self.attack_time >= self.attacking_cooldown:
                self.is_attacking = False

        if self.is_object_interacting:
            if current_time - self.object_interacting_time >= 100:
                self.is_object_interacting = False

        if not self.attack_available:
            if current_time - self.attack_time >= self.attack_again_cooldown:
                self.attack_available = True

        if not self.shield_available:
            if current_time - self.shield_time >= self.shield_again_cooldown:
                self.shield_available = True

    def handle_item_touch(self) -> None:
        for item in self.items_sprite_group:
            if item.interact_ratio.colliderect(self.hitbox):
                item.on_touched(self)       

    def update(self) -> None:   
        if not self.disabled:
            self.handle_inputs()
            self.handle_status()
            self.cooldowns() 
            self.animate()
            self.handle_item_touch()
            self.move(self.speed)
        else:
            self.animate()