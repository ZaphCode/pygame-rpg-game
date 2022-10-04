from dataclasses import dataclass

@dataclass
class UserStats:
    health: int
    max_speed: int
    damage: int

@dataclass
class EnemyStats:
    health: int
    speed: int
    damage: int
    attack_cooldown: int
    notice_ratio: int
    attack_ratio: int
    scale: float = 2.5

    