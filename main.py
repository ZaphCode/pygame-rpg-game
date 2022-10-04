import pygame
from level import Level
from menu import Menu
from modal import Modal
from settings import *
from sys import exit
from debug import debugger

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("RGP Test")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.status: str = "main_menu" 
        self.level = Level(self.set_game_status)
        self.main_menu = Menu(self.set_game_status)
        self.pause_modal = Modal(self.set_game_status)
    
    def run(self) -> None:
        while True:
            self.handle_events() # Event loop

            if self.status == "main_menu":
                self.screen.fill("#1D1815")
                self.main_menu.render()
            elif self.status == "playing":
                self.screen.fill("#25131a")
                self.level.run()
            elif self.status == "gameover":
                self.screen.fill("#1D1815")
            elif self.status == "paused":
                self.pause_modal.render()
            elif self.status == "exit":
                self.exit()

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

    def set_game_status(self, status: str):
        self.status = status
                        
    def exit(self) -> None:
        pygame.quit()
        exit()

if __name__ == "__main__":
    Game().run()