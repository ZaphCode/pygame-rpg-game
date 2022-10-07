from lib.stats import EnemyStats, PlayerStats

WIDTH = 480 * 1.5
HEIGHT = 320 * 1.5
FPS = 60
TILESIZE = 32
DEBUG_FONT_COLOR = (180, 180, 255, 80)
MAIN_FONT_SRC = "./assets/pixel_font.ttf"
TITLE_FONT_SRC = "./assets/pixel_font_2.ttf"

PLAYER_DEFAULT_STATS = PlayerStats(
    health=500,
    speed=3,
    damage=50
)

ENEMYS = {
    "spider": EnemyStats(
        health=100,
        speed=3,
        damage=35,
        attack_cooldown=1000,
        notice_ratio=140,
        attack_ratio=30,
        scale=2.2
    ),
    "phantom": EnemyStats(
        health=150,
        speed=2,
        damage=45,
        attack_cooldown=1300,
        notice_ratio=180,
        attack_ratio=30,
    ),
    "slime": EnemyStats(
        health=250,
        speed=2,
        damage=50,
        attack_cooldown=1400,
        notice_ratio=140,
        attack_ratio=30,
        scale=3,
        loot_items=["health_potion", "health_potion", None],
        frame_change_speed=0.1
    ),
    "spinner": EnemyStats(
        health=350,
        speed=2,
        damage=50,
        attack_cooldown=1300,
        notice_ratio=180,
        attack_ratio=30,
        scale=3
    ),
    "bat": EnemyStats(
        health=100,
        speed=3,
        damage=25,
        attack_cooldown=1300,
        notice_ratio=110,
        attack_ratio=30,
    ),
    "bat_boss": EnemyStats(
        health=1000,
        speed=2,
        damage=60,
        attack_cooldown=1700,
        notice_ratio=220,
        attack_ratio=71,
        scale=6,
        loot_items=["golden_key"],
        frame_change_speed=0.1
    )
}
