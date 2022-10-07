from typing import List
import pygame
from settings import MAIN_FONT_SRC

pixel_font = pygame.font.Font(MAIN_FONT_SRC, 18)

class Button(pygame.sprite.Sprite):
    def __init__(self, type: str, text: str, position, groups: List[pygame.sprite.Group], on_click_fn = None, custom_size = None) -> None:
        super().__init__(groups)
        self.type = type
        self.position = position
        self.on_click_fn = on_click_fn
        self.custom_size = custom_size
        self.image = pygame.image.load(f"assets/ui/buttons/btn-lg.png").convert_alpha()
        self.scale_btn()
        self.rect = self.image.get_rect(center = position)
        self.text = pixel_font.render(text, False, "White")
        self.text_rect = self.text.get_rect(center = (position[0], position[1] - 3))
        
    def scale_btn(self) -> None:
        if self.custom_size:
            self.image = pygame.transform.scale(self.image, self.custom_size)
        else:
            scale = (0, 0)
            if "sm" in self.type: scale = (45, 60)
            elif "md" in self.type: scale = (100, 60),
            elif "lg" in self.type: scale = (180, 60)
            self.image = pygame.transform.scale(self.image, scale)

    def handle_hover(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.image.load(f"assets/ui/buttons/btn-lg-hover.png").convert_alpha()
            self.scale_btn()
        else:
            self.image = pygame.image.load(f"assets/ui/buttons/btn-lg.png").convert_alpha()
            self.scale_btn()

    def handle_click(self) -> None:
        if self.on_click_fn:
            click = pygame.mouse.get_pressed()[0]
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if click:
                    self.on_click_fn()

    def update(self) -> None:
        self.handle_click()
        self.handle_hover()