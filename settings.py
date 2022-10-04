from lib.stats import EnemyStats

WIDTH = 480 * 1.5
HEIGHT = 320 * 1.5
FPS = 60
TILESIZE = 32
PLAYER_SPEED = 4
DEBUG_FONT_COLOR = (180, 180, 255, 80)
MAIN_FONT_SRC = "./assets/pixel_font.ttf"

ENEMYS = {
    "bat": EnemyStats(
        health=100,
        speed=2,
        damage=35,
        attack_cooldown=1000,
        notice_ratio=170,
        attack_ratio=30,
    ),
}
