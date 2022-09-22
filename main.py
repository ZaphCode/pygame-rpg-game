import pygame
from level import Level
from settings import *
from sys import exit
from debug import debugger

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("RGP Test")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.level = Level()
    
    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: debugger.active = not debugger.active
            
            self.screen.fill("Gray")
            self.level.run()

            debugger.show(pygame.mouse.get_pos())

            pygame.display.update()
            self.clock.tick(FPS)

    def exit(self) -> None:
        self.running = False
        pygame.quit()
        exit()

if __name__ == "__main__":
    Game().run()