from typing import List, Tuple
import pygame

class DemonChort(pygame.sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int],
        groups: List[pygame.sprite.Group], 
        disabled: bool = False
    ) -> None:
        super().__init__(groups)
        self.image = self.image = pygame.image.load("assets/demons/chort/chort_idle_anim_f0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.frame_index: int = 0

    def animate(self) -> None:
        static_frames = [
            pygame.image.load("assets/demons/chort/chort_idle_anim_f0.png").convert_alpha(),
            pygame.image.load("assets/demons/chort/chort_idle_anim_f1.png").convert_alpha(),
            pygame.image.load("assets/demons/chort/chort_idle_anim_f2.png").convert_alpha(),
            pygame.image.load("assets/demons/chort/chort_idle_anim_f3.png").convert_alpha(),
        ]

        self.frame_index += 0.1
        if self.frame_index >= len(static_frames): self.frame_index = 0
        image = static_frames[int(self.frame_index)]
        image = pygame.transform.scale(image, (60, 80))
        image = pygame.transform.flip(image, True, False)
        self.image = image


    def update(self) -> None:
        self.animate()