import pygame
from lib.files import import_folder
from lib.stats import EnemyStats
from settings import ENEMYS
from sprites.entity import Entity
import pygame
from sprites.item import Item
from sprites.player import Player
from typing import List, Tuple
from pygame.transform import flip
from random import choice

class Enemy(Entity):
    def __init__(
        self, 
        enemy_type: str,
        position: Tuple[float, float],
        groups: List[pygame.sprite.Group], 
        obstacle_sprites_group: pygame.sprite.Group,
        player: Player,
        create_item_fn
    ) -> None:
        super().__init__(groups, obstacle_sprites_group)
        self.create_item_fn = create_item_fn
        # Graphics
        if "_boss" in enemy_type: 
            self.enemy_type_src = enemy_type.replace("_boss", "")
            self.is_boss = True
        else: 
            self.is_boss = False
            self.enemy_type_src: str = enemy_type 
        self.frame_index = 0
        self.status = "idle"
        self.heading_side = "left"
        self.stats: EnemyStats = ENEMYS[enemy_type]
        self.current_health = self.stats.health
        self.current_frame_change_speed = self.stats.frame_change_speed
        self.load_animations()
        self.image = self.animations[self.status][self.frame_index]
        # Movement
        self.rect = self.image.get_rect(center = position)
        self.hitbox = self.rect.inflate(-10, -10)
        self.player = player
        # Actions
        self.is_attacking: bool = False
        self.attack_available = True
        self.attack_available_time = None
        self.attack_available_cooldown= 1000
        self.last_attack_direction = pygame.math.Vector2()
        # Hits
        self.attacked: bool = False
        self.attacked_time = None
        self.attacked_cooldown = 250

    def load_animations(self) -> None:
        self.animations: dict = {
            "idle": [], "walking": [], "hit": [], "dead": []
        }

        for animation in self.animations.keys():
            path = f"assets/enemys/{self.enemy_type_src}/{animation}"
            self.animations[animation] = import_folder(path, self.stats.scale)

    def get_player_distance_and_direction(self, player: Player) -> Tuple[float, pygame.math.Vector2]:
        enemy_vect = pygame.math.Vector2(self.rect.center)
        player_vect = pygame.math.Vector2(player.rect.center)
        distance = (player_vect - enemy_vect).magnitude()
        if distance > 0: direction = (player_vect - enemy_vect).normalize()
        else: direction = pygame.math.Vector2() 
        return (distance, direction)
    
    def get_status(self) -> None:
        if self.current_health <= 0:
            self.status = "dead"
            return

        if self.attacked:
            self.status = "hit"
            return

        if self.direction != pygame.math.Vector2():
            if self.direction.x:
                if self.direction.x > 0: self.heading_side = "left"
                else: self.heading_side = "right"
            self.status = "walking"
        else:
            self.status = "idle"

    def handle_actions(self, player: Player) -> None:
        distance, direction = self.get_player_distance_and_direction(player)

        if self.current_health <= 0:
            self.direction = pygame.math.Vector2()
            if int(self.frame_index) >= len(self.animations[self.status]) - 1:
                drop = choice(list(self.stats.loot_items))
                if drop:
                    if self.is_boss: self.create_item_fn(drop, self.hitbox.center - pygame.math.Vector2(0, 20))
                    else: self.create_item_fn(drop, self.hitbox.topleft)
                self.kill()
            return   

        # Attacked knockback
        if self.attacked:
            self.current_frame_change_speed = 0.2
            self.direction = direction.rotate(180)
            return
        else:
            self.current_frame_change_speed = self.stats.frame_change_speed

        # Dispatch attack
        if distance <= self.stats.attack_ratio:
            if self.attack_available:
                self.attack(player)
                self.attack_available_time = pygame.time.get_ticks()
                self.attack_available = False    
        
        # Movement
        if distance <= self.stats.notice_ratio and self.attack_available:
            self.last_attack_direction = direction
            self.direction = direction
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self) -> None:
        current_time = pygame.time.get_ticks()

        if not self.attack_available:
            if current_time - self.attack_available_time >= self.stats.attack_cooldown:
                self.attack_available = True

        if self.attacked:
            if current_time - self.attacked_time >= self.attacked_cooldown:
                self.attacked = False
    
    def animate(self) -> None:
        current_animation: List[pygame.Surface] = self.animations[self.status]
        self.frame_index += self.stats.frame_change_speed
        if self.frame_index >= len(current_animation): self.frame_index = 0
        if self.heading_side == "left": self.image = flip(current_animation[int(self.frame_index)], True, False)
        elif self.heading_side == "right": self.image = current_animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def attack(self, player: Player) -> None:
        if not player.attacked:
            if not player.is_shielded:
                player.attacked_time = pygame.time.get_ticks()
                player.attacked = True
                player.frame_index = 0
                player.current_health -= self.stats.damage
                player.direction = self.last_attack_direction
            else:
                print("attack missed")

    def update(self) -> None:
        self.get_status()
        self.cooldowns()
        self.handle_actions(self.player)
        self.animate()
        self.move(self.stats.speed)