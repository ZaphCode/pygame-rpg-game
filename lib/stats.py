from dataclasses import dataclass
from typing import List

@dataclass
class PlayerStats:
    health: int
    speed: int
    damage: int
    frame_change_speed: float = 0.2

@dataclass
class EnemyStats:
    health: int
    speed: int
    damage: int
    attack_cooldown: int
    notice_ratio: int
    attack_ratio: int
    scale: float = 2.5
    loot_items: any = ("crystal", None, None)
    frame_change_speed: float = 0.2

    