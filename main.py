import pygame
from displays.level import Level
from displays.menu import Menu
from displays.pause import Pause
from displays.gameover import Gameover
from displays.win import Win
from settings import *
from sys import exit
from lib.sounds import sounds_manager
from debug import debugger

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("RGP Test")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.status: str = "main_menu" 
        self.level = Level((162, 1408), (1807, 650), self.set_game_status)
        self.main_menu = Menu(self.set_game_status)
        self.pause_modal = Pause(self.set_game_status)
        self.gameover = Gameover(self.set_game_status)
        self.winscreen = Win(self.set_game_status)
    
    def run(self) -> None:
        while True:
            self.handle_events() # Event loop

            if self.status == "main_menu":
                self.main_menu.render()
            elif self.status == "playing":
                self.screen.fill("#25131a")
                self.level.run()
            elif self.status == "gameover":
                self.gameover.render()
            elif self.status == "paused":
                self.pause_modal.render()
            elif self.status == "restart":
                self.level = Level((162, 1408), (1807, 650), self.set_game_status)
                self.set_game_status("playing")
            elif self.status == "win":
                self.winscreen.render()
            elif self.status == "exit":
                self.exit()

            self.handle_music()

            debugger.show(f"status: {self.status}", 10, 10)
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: debugger.active = not debugger.active

                if event.key == pygame.K_ESCAPE: 
                    if self.status == "playing": self.set_game_status("paused")
                    elif self.status == "paused": self.set_game_status("playing")

                if event.key == pygame.K_SPACE and self.status == "main_menu":
                    self.set_game_status("playing")

    def handle_music(self) -> None:
        if self.status == "main_menu":
            sounds_manager.play_main_menu_song()
        elif self.status == "playing" or self.status == "paused":
            sounds_manager.win_song.stop()
            sounds_manager.main_menu_song.stop()
            sounds_manager.gameover_song.stop()
            sounds_manager.play_playing_song()
        elif self.status == "win":
            sounds_manager.playing_song.stop()
            sounds_manager.play_win_song()
        elif self.status == "gameover":
            sounds_manager.playing_song.stop()
            sounds_manager.play_gameover_song()
        elif self.status == "restart":
            sounds_manager.playing_song_played = False
            sounds_manager.win_song_played = False
            sounds_manager.gameover_song_played = False

    def set_game_status(self, status: str):
        self.status = status
                        
    def exit(self) -> None:
        pygame.quit()
        exit()

if __name__ == "__main__":
    Game().run()