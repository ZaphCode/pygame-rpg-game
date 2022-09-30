import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] / 2
        self.half_h = self.display_surface.get_size()[1] / 2
        self.offset = pygame.math.Vector2()

    def _draw(self, player: pygame.sprite.Sprite) -> None:
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery -  self.half_h

        for sprite in self.sprites():
            offset_post = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, dest=offset_post)

class YSortedCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] / 2
        self.half_h = self.display_surface.get_size()[1] / 2
        self.offset = pygame.math.Vector2()

    def _draw(self, player: pygame.sprite.Sprite) -> None:
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery -  self.half_h

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_post = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, dest=offset_post)