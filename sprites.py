import pygame


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scale_down=1):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // scale_down, height // scale_down))
        return image


class SingleAnimation(pygame.sprite.Sprite):
    def __init__(self, center, spritesheet, frame_rate):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.image = spritesheet[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.spritesheet):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.spritesheet[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center