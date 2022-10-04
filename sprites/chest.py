from sprites.item import Item
from sprites.player import Player
import pygame

class Chest(Item):
    def __init__(
        self, 
        loot_type: str,
        position,
        groups, 
    ) -> None:
        super().__init__("chest", position, groups, 2, 0.1, False)
        self.item_groups = groups
        self.loot_type = loot_type
        self.interact_ratio = self.rect.inflate(18, 18)

    def on_touched(self, player: Player):
        keys = pygame.key.get_pressed()
        player.object_interacting_time = pygame.time.get_ticks()
        player.is_object_interacting = True
        if keys[pygame.K_SPACE] and not self.touched:
            self.frame_index = 0
            self.animation_speed = 0.3
            self.hitbox = self.hitbox.inflate(-10, -10)
            self.touched = True
            Item(self.loot_type, self.rect.topleft, self.item_groups[:2])
        
        