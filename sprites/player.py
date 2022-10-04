from typing import List, Tuple
import pygame
from lib.files import import_folder
from settings import *
from sprites.entity import Entity

class Player(Entity):
    def __init__(
        self, 
        position: Tuple[float, float], 
        groups: List[pygame.sprite.Group],
        obstacle_sprites_group: pygame.sprite.Group,
        items_sprite_group: pygame.sprite.Group,
        create_attack_function,
        disabled: bool = False,
        scale: float = 2.8
    ) -> None:
        super().__init__(groups, obstacle_sprites_group)
        self.stats = PLAYER_DEFAULT_STATS
        # Level utils
        self.obstacle_sprites_group = obstacle_sprites_group
        self.items_sprite_group = items_sprite_group
        self.create_attack_function = create_attack_function
        # Animation
        self.frame_index: int = 0
        self.current_frame_change_speed = self.stats.frame_change_speed
        self.status: str = "down_idle"
        self.last_heanding: str = "down"
        self.load_animations(scale)
        self.image = self.animations[self.status][self.frame_index]
        # Movement
        self.current_speed: int = self.stats.speed
        self.disabled = disabled
        self.rect = self.image.get_rect(center = position)
        self.hitbox = self.rect.inflate(-6, -16)
        # Attacking
        self.is_attacking: bool = False
        self.attack_available: bool = False
        self.attacking_cooldown: int = 200
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
        # Enemy interactions
        self.is_dead: bool = False
        self.current_health: int = self.stats.health
        self.attacked: bool = False
        self.attacked_time = None
        self.attacked_cooldown: int = 300

    def load_animations(self, scale) -> None:
        self.animations: dict = {
            "up": [], "down": [], "right": [], "left": [],
            "up_idle": [], "down_idle": [], "right_idle": [], "left_idle": [],
            "up_attack": [], "down_attack": [], "right_attack": [], "left_attack": [],
            "up_shielded": [], "down_shielded": [], "right_shielded": [], "left_shielded": [],
            "up_hit": [], "down_hit": [], "right_hit": [], "left_hit": [],
            "dead": []
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"assets/player/{animation}", scale)

    def animate(self) -> None:
        current_animation: List[pygame.Surface] = self.animations[self.status]
        self.frame_index += self.current_frame_change_speed
        if self.frame_index >= len(current_animation): self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def handle_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.is_attacking and not self.is_shielded and not self.attacked:
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
        
        if keys[pygame.K_SPACE] and self.attack_available and not self.is_shielded and not self.is_object_interacting and not self.attacked:
            self.is_attacking = True
            self.frame_index = 0
            self.attack_available = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack_function()

        if keys[pygame.K_LCTRL]:
            if not self.is_attacking and self.shield_available and not self.attacked:
                self.is_shielded = True
                self.shield_available = False
                self.shield_time = pygame.time.get_ticks()
        else:
            self.is_shielded = False

    def handle_status(self):
        if self.current_health <= 0:
            self.direction = pygame.math.Vector2()
            self.status = "dead"
            if int(self.frame_index) >= len(self.animations[self.status]) - 1:
                self.is_dead = True
            return

        if self.is_attacking:
            self.current_speed = self.stats.speed / 2
            self.current_frame_change_speed = self.stats.frame_change_speed * 1.8
            if not "attack" in self.status:
                self.status = self.last_heanding + "_attack"
        else: 
            self.current_speed = self.stats.speed
            self.current_frame_change_speed = self.stats.frame_change_speed
            self.status = self.last_heanding

        if self.attacked:
            if not "hit" in self.status:
                self.status = self.last_heanding + "_hit"

        if self.is_shielded: 
            self.direction.x = 0
            self.direction.y = 0
            if not "shielded" in self.status:
                self.status = self.last_heanding + "_shielded"

        if self.direction.x == 0 and self.direction.y == 0: #idle
            if not "idle" in self.status and not self.is_shielded and not self.is_attacking and not self.attacked: 
                self.status = self.last_heanding + "_idle"
               
    def cooldowns(self) -> None:
        current_time = pygame.time.get_ticks()

        if self.is_attacking:
            if current_time - self.attack_time >= self.attacking_cooldown:
                self.is_attacking = False

        if self.attacked:
            if current_time - self.attacked_time >= self.attacked_cooldown:
                self.attacked = False

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
            self.move(self.current_speed)
        else:
            self.animate()