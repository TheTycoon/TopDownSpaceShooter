import pygame
import random
import enemies
import settings


class Level:
    def __init__(self, game):
        self.game = game
        self.total_waves = 3
        self.current_wave = 1
        self.wave_duration = 10000
        self.wave_timer = pygame.time.get_ticks()

        self.enemy_update = pygame.time.get_ticks()

        # self.destination_image = pygame.

    def update_level(self):
        now = pygame.time.get_ticks()

        if now - self.wave_timer > self.wave_duration:
            self.wave_timer = now
            self.current_wave += 1

        if self.current_wave == 1:
            if now - self.enemy_update > 100:
                self.enemy_update = now
                size_list = ['small', 'medium', 'large']
                size = random.choice(size_list)
                enemies.Asteroid(self.game, size)
        elif self.current_wave == 2:
            if now - self.enemy_update > 5000:
                self.enemy_update = now
                random_position = random.randint(200, settings.WIDTH - 200)
                swarm = [enemies.Mob(self.game, random_position, -100),
                         enemies.Mob(self.game, random_position + 50, -150),
                         enemies.Mob(self.game, random_position - 50, -150),
                         enemies.Mob(self.game, random_position + 100, -200),
                         enemies.Mob(self.game, random_position - 100, -200)]
        elif self.current_wave >= 3:
            if now - self.enemy_update > 3000:
                self.enemy_update = now
                if random.randint(0, 1) == 0:
                    enemies.GroundLaser(self.game, settings.WIDTH - 200, -50, 'left')
                else:
                    enemies.GroundLaser(self.game, 200, -50, 'right')




