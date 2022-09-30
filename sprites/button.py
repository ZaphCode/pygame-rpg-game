from typing import List
import pygame

pixel_font = pygame.font.Font("./assets/pixel_font.ttf", 18)

class Button(pygame.sprite.Sprite):
    def __init__(self, size: str, text: str, pos, groups: List[pygame.sprite.Group], on_click_fn = None) -> None:
        super().__init__(groups)
        
        self.size = size
        self.pos = pos
        self.on_click_fn = on_click_fn

        if self.size == "lg":
            self.image = pygame.image.load("./assets/ui/ui-btn-lg.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (180, 60))
        elif self.size == "sm":
            self.image = pygame.image.load("./assets/ui/ui-btn-sm.png").convert_alpha()
            self.image = pygame.transform.scale2x(self.image)

        self.rect = self.image.get_rect(center = pos)

        self.text = pixel_font.render(text, False, "White")
        self.text_rect = self.text.get_rect(center = (pos[0], pos[1] - 3))
        
    def handle_hover(self) -> None:
        if self.size == "lg":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = pygame.image.load("./assets/ui/ui-btn-lg-hover.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (180, 60))
            else:
                self.image = pygame.image.load("./assets/ui/ui-btn-lg.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (180, 60))

    def handle_click(self) -> None:
        if self.on_click_fn:
            click = pygame.mouse.get_pressed()[0]
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if click:
                    self.on_click_fn()

    def update(self) -> None:
        self.handle_click()
        self.handle_hover()