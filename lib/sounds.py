import pygame
pygame.init()

class SoundsManager:
    def __init__(self) -> None:
        sounds_path = "assets/sounds"
        # Pops
        self.sword_slash = pygame.mixer.Sound(sounds_path+"/sword_slash.mpeg")
        self.sword_slash.set_volume(0.45)
        self.crystal_picked = pygame.mixer.Sound(sounds_path+"/crystal_picked.mpeg")
        self.crystal_picked.set_volume(3)
        self.player_hit = pygame.mixer.Sound(sounds_path+"/player_hit.mpeg")
        self.player_hit.set_volume(4)
        self.open_door = pygame.mixer.Sound(sounds_path+"/open_door.mpeg")
        self.open_door.set_volume(5)
        self.player_dead = pygame.mixer.Sound(sounds_path+"/player_dead.mpeg")
        self.block_shield = pygame.mixer.Sound(sounds_path+"/block-shield.mp3")
        self.block_shield.set_volume(0.28)
        self.speed_potion = pygame.mixer.Sound(sounds_path+"/speed_potion.mp3")
        self.speed_potion.set_volume(0.5)
        self.health_potion = pygame.mixer.Sound(sounds_path+"/health_potion.mp3")
        self.health_potion.set_volume(0.6)
        self.key_pick = pygame.mixer.Sound(sounds_path+"/key_pick.mp3")
        self.open_chest = pygame.mixer.Sound(sounds_path+"/open_chest.mp3")
        self.open_chest.set_volume(40)
        # Songs
        self.playing_song_played = False
        self.playing_song= pygame.mixer.Sound(sounds_path+"/playing_song.mp3")

        self.main_menu_song_played = False
        self.main_menu_song = pygame.mixer.Sound(sounds_path+"/main_menu_song.mp3")

        self.win_song_played = False
        self.win_song = pygame.mixer.Sound(sounds_path+"/win_song.mp3")

        self.gameover_song_played = False
        self.gameover_song = pygame.mixer.Sound(sounds_path+"/gameover_song.mp3")

    def play_playing_song(self) -> None:
        if not self.playing_song_played:
            self.playing_song.play(loops=-1)
            self.playing_song.set_volume(0.37)
            self.playing_song_played = True
        
    def play_main_menu_song(self) -> None:
        if not self.main_menu_song_played:
            self.main_menu_song.play(loops=-1)
            self.main_menu_song.set_volume(0.3)
            self.main_menu_song_played = True

    def play_win_song(self) -> None:
        if not self.win_song_played:
            self.win_song.play(loops=-1)
            self.win_song.set_volume(0.2)
            self.win_song_played = True

    def play_gameover_song(self) -> None:
        if not self.gameover_song_played:
            self.gameover_song.play(loops=-1)
            self.gameover_song.set_volume(0.2)
            self.gameover_song_played = True


sounds_manager = SoundsManager()