import pygame
import settings
import random


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_image
        self.image.set_colorkey(settings.BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_hull = 50
        self.current_hull = 50
        self.banking_speed = 0
        self.thrusting_speed = 3

    def update(self):
        self.rect.x += self.banking_speed
        self.rect.y += self.thrusting_speed

        if self.rect.top > settings.HEIGHT or self.rect.right < 0 or self.rect.left > settings.WIDTH:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game, size, from_death=False, death_rect=pygame.Rect(0, 0, 0, 0)):
        self.groups = game.asteroids
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = size
        if self.size == 'large':
            self.spritesheet = game.asteroid_frames_large
            self.max_hull = 100
            self.current_hull = 100
        elif self.size == 'medium':
            self.spritesheet = game.asteroid_frames_medium
            self.max_hull = 50
            self.current_hull = 50
        elif self.size == 'small':
            self.spritesheet = game.asteroid_frames_small
            self.max_hull = 25
            self.current_hull = 25

        self.current_frame = 0
        self.frame_rate = random.randint(50, 100)
        self.rotation = random.randint(0, 1)
        self.last_update = pygame.time.get_ticks()
        self.image = self.spritesheet[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        if from_death:
            self.rect.x = death_rect.x + random.randint(-5, 5)
            self.rect.y = death_rect.y + random.randint(-5, 5)
        else:
            self.rect.x = random.randint(50, settings.WIDTH - 50)
            self.rect.y = -100
        self.banking_speed = random.randint(-2, 2)
        self.thrusting_speed = random.randint(1, 3)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.rotation == 0:
                self.current_frame = (self.current_frame + 1) % len(self.spritesheet)
            else:
                self.current_frame = (self.current_frame - 1) % len(self.spritesheet)

            center = self.rect.center
            self.image = self.spritesheet[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

        self.rect.x += self.banking_speed
        self.rect.y += self.thrusting_speed

        if self.rect.top > settings.HEIGHT or self.rect.right < 0 or self.rect.left > settings.WIDTH:
            self.kill()


class GroundLaser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.direction = direction
        if self.direction == 'left':
            self.image = game.ground_enemy_image_left
        elif self.direction == 'right':
            self.image = game.ground_enemy_image_right
        self.image.set_colorkey(settings.BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_hull = 10000
        self.current_hull = 10000

        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += 1

        now = pygame.time.get_ticks()
        if now - self.last_shot > 1000:
            self.last_shot = now
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self.direction, 5)
            self.game.enemy_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.player_bullet_image
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speed = pygame.math.Vector2(0, 1)
        if direction == 'up':
            self.speed.y += -speed
        elif direction == 'down':
            self.speed.y += speed
        elif direction == 'left':
            self.speed.x += -speed
        elif direction == 'right':
            self.speed.x += speed

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y +=  self.speed.y

        # gets rid of bullet once it is off screen
        if self.rect.bottom < 0 or self.rect.top > settings.HEIGHT or self.rect.left > settings.WIDTH or self.rect.right < 0 :
            self.kill()



DART_ENEMY = {
    'hull': 25,
    'shield': 0,
    'banking': 0,
    'thrusting': 3
}