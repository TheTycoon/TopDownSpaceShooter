import pygame
import settings
import sprites
import weapons


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        temp_image = self.game.player_image
        temp_rect = temp_image.get_rect()
        self.not_banking_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
        self.image = self.not_banking_image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.mask = pygame.mask.from_surface(temp_image)

        temp_image = self.game.player_bank_right_image
        temp_rect = temp_image.get_rect()
        self.bank_right_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
        self.banking_right = False

        temp_image = self.game.player_bank_left_image
        temp_rect = temp_image.get_rect()
        self.bank_left_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
        self.banking_left = False

        self.ship = settings.PLAYER_SHIP_3

        self.max_hull = self.ship['hull']
        self.current_hull = self.ship['hull']
        self.max_shield = self.ship['shield']
        self.current_shield = self.ship['shield']
        self.thrust = self.ship['thrust']
        self.banking_magnitude = self.ship['banking']

        self.weapon_slots = self.ship['weapon slots']
        self.weapon_rects = []
        self.update_weapon_rects()

        self.last_shot1 = pygame.time.get_ticks()
        self.shoot_delay1 = 500
        self.joystick_firing1 = False
        self.last_shot2 = pygame.time.get_ticks()
        self.shoot_delay2 = 500
        self.joystick_firing2 = False
        self.last_shot3 = pygame.time.get_ticks()
        self.shoot_delay3 = 500
        self.joystick_firing3 = False



        self.invulnerable = False
        self.damage_cooldown = 1000
        self.cooldown_timer = pygame.time.get_ticks()

    def update(self):
        self.speed = pygame.math.Vector2(0, 0)
        self.move()
        self.update_weapon_rects()
        self.shoot()
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if now - self.cooldown_timer > self.damage_cooldown:
                self.invulnerable = False

        if self.banking_right:
            self.image = self.bank_right_image
        elif self.banking_left:
            self.image = self.bank_left_image
        else:
            self.image = self.not_banking_image

        self.mask = pygame.mask.from_surface(self.image)

    def update_weapon_rects(self):
        self.weapon_rects = []
        if self.weapon_slots == 1 or self.weapon_slots == 3:
            weapon_rect1 = self.rect.copy()
            self.weapon_rects.append(weapon_rect1)
        if self.weapon_slots == 2:
            weapon_rect1 = self.rect.copy()
            weapon_rect1.x -= 15
            self.weapon_rects.append(weapon_rect1)
            weapon_rect2 = self.rect.copy()
            weapon_rect2.x += 15
            self.weapon_rects.append(weapon_rect2)
        if self.weapon_slots == 3:
            weapon_rect2 = self.rect.copy()
            weapon_rect2.x += 25
            self.weapon_rects.append(weapon_rect2)
            weapon_rect3 = self.rect.copy()
            weapon_rect3.x -= 25
            self.weapon_rects.append(weapon_rect3)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.banking_right = False
        self.banking_left = False

        keystate = pygame.key.get_pressed()

        joystick_horizontal = 0
        joystick_vertical = 0
        if self.game.joystick_enabled:
            joystick_horizontal = self.game.joystick.get_axis(settings.JOYAXIS['LeftHorizontal'])
            joystick_vertical = self.game.joystick.get_axis(settings.JOYAXIS['LeftVertical'])

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a] or joystick_horizontal < -0.5:
            self.speed.x = -self.banking_magnitude
            self.banking_left = True
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d] or joystick_horizontal > 0.5:
            self.speed.x = self.banking_magnitude
            self.banking_right = True
        if keystate[pygame.K_UP] or keystate[pygame.K_w] or joystick_vertical < -0.5:
            self.speed.y = -self.thrust
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s] or joystick_vertical > 0.5:
            self.speed.y = self.thrust

        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

        if self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.HEIGHT:
            self.rect.bottom = settings.HEIGHT

    def enemy_collision(self):
        self.current_hull -= 10
        if self.current_hull <= 0:
            self.death()
        else:
            self.game.explosions.add(sprites.SingleAnimation(self.rect.center, self.game.explosion_frames, 50))
        self.invulnerable = True
        self.cooldown_timer = pygame.time.get_ticks()

    # include some sort of death screen / state
    def death(self):
        self.game.explosions.add(sprites.SingleAnimation(self.rect.center, self.game.death_explosion_frames, 50))

    def shoot(self):
        if self.joystick_firing1:
            now = pygame.time.get_ticks()
            if now - self.last_shot1 > self.shoot_delay1:
                self.last_shot1 = now
                weapons.fire_machine_gun(self.game, self.weapon_rects[0], 3)
        if self.joystick_firing2:
            now = pygame.time.get_ticks()
            if now - self.last_shot2 > self.shoot_delay2:
                self.last_shot2 = now
                weapons.fire_machine_gun(self.game, self.weapon_rects[1], 3)
        if self.joystick_firing3:
            now = pygame.time.get_ticks()
            if now - self.last_shot3 > self.shoot_delay3:
                self.last_shot3 = now
                weapons.fire_machine_gun(self.game, self.weapon_rects[2], 3)




    # def shoot(self):
    #     keystate = pygame.key.get_pressed()
    #
    #     if self.weapon_slots == 1:
    #         if keystate[pygame.K_1]:
    #             now = pygame.time.get_ticks()
    #             if now - self.last_shot1 > self.shoot_delay1:
    #                 self.last_shot1 = now
    #                 self.joystick_firing = True
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[0], 1, now)
    #
    #     elif self.weapon_slots == 2:
    #         if keystate[pygame.K_1]:
    #             now = pygame.time.get_ticks()
    #             if now - self.last_shot1 > self.shoot_delay1:
    #                 self.last_shot1 = now
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[0], 3, now)
    #         if keystate[pygame.K_2]:
    #             now = pygame.time.get_ticks()
    #             if now - self.last_shot2 > self.shoot_delay2:
    #                 self.last_shot2 = now
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[1], 3, now)
    #     elif self.weapon_slots == 3:
    #         if keystate[pygame.K_1]:
    #             now1 = pygame.time.get_ticks()
    #             if now1 - self.last_shot1 > self.shoot_delay1:
    #                 self.last_shot1 = now1
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[0], 3, now1)
    #         if keystate[pygame.K_2]:
    #             now2 = pygame.time.get_ticks()
    #             if now2 - self.last_shot2 > self.shoot_delay2:
    #                 self.last_shot2 = now2
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[1], 3, now2)
    #         if keystate[pygame.K_3]:
    #             now3 = pygame.time.get_ticks()
    #             if now3 - self.last_shot3 > self.shoot_delay3:
    #                 self.last_shot3 = now3
    #                 weapons.fire_machine_gun(self.game, self.weapon_rects[2], 3, now3)

    def joystick_button(self, event):
        if self.weapon_slots >= 1:
            if event.button == settings.JOYBUTTONS['A'] and event.type == pygame.JOYBUTTONDOWN:
                self.joystick_firing1 = True
            if event.button == settings.JOYBUTTONS['A'] and event.type == pygame.JOYBUTTONUP:
                self.joystick_firing1 = False

        if self.weapon_slots >= 2:
            if event.button == settings.JOYBUTTONS['X'] and event.type == pygame.JOYBUTTONDOWN:
                self.joystick_firing2 = True
            if event.button == settings.JOYBUTTONS['X'] and event.type == pygame.JOYBUTTONUP:
                self.joystick_firing2 = False

        if self.weapon_slots >= 3:
            if event.button == settings.JOYBUTTONS['Y'] and event.type == pygame.JOYBUTTONDOWN:
                self.joystick_firing3 = True
            if event.button == settings.JOYBUTTONS['Y'] and event.type == pygame.JOYBUTTONUP:
                self.joystick_firing3 = False







class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.player_bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -7

    def update(self):
        # updates position based on speed
        self.rect.y +=  self.speed_y

        # gets rid of bullet once it is off screen
        if self.rect.bottom < 0:
            self.kill()



