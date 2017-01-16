import pygame
import settings
from os import path
import player
import enemies
import levels
import sprites
from transitions import Machine
import button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse
        # Detects and initializes a joystick if there is one connected
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.init()
            self.joystick_enabled = True
        else:
            self.joystick_enabled = False

        # State Machine
        states = ['start screen', 'options menu', 'playing', 'paused']
        transitions = [
            {'trigger': 'new', 'source': 'start screen', 'dest': 'playing'},
            {'trigger': 'options', 'source': 'start screen', 'dest': 'options menu'}
        ]
        self.machine = Machine(states=states, transitions=transitions, initial='start screen')

        # buttons for the start screen, consider moving later
        self.buttons = []
        self.start_button = button.StartButton(self, settings.WIDTH / 2 - 150, settings.HEIGHT / 2 - 150, 300, 100, 'Start')
        self.buttons.append(self.start_button)
        self.options_button = button.Button(self, settings.WIDTH / 2 - 150, settings.HEIGHT / 2, 300, 100, 'Options')
        self.buttons.append(self.options_button)
        self.exit_button = button.ExitButton(self, settings.WIDTH / 2 - 150, settings.HEIGHT / 2 + 150, 300, 100, 'Exit')
        self.buttons.append(self.exit_button)

        # Sprite Groups: Need to be Updated, Drawn... also used for collision detections
        self.player_sprite = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.background_stars = pygame.sprite.Group()

    def new(self):
        # Flag indicating the application is running
        self.running = True
        # Load all images/sounds/etc for the game
        self.load_data()

        # temporarily being used to load level, spawn player and enemies, remove later once levels are added
        self.level_one = levels.Level(self)
        self.player = player.Player(self, settings.WIDTH / 2, 7 * settings.HEIGHT / 8)

        self.enemy_update = pygame.time.get_ticks() # move somewhere better
        self.star_update = pygame.time.get_ticks()  # move somewhere better

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()

    def load_data(self):
        # Easy names for file directories
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.snd_folder = path.join(self.game_folder, 'snd')

        # SINGLE IMAGES BELOW
        self.player_image = pygame.image.load(path.join(self.img_folder, "player_ship_1_gun.png")).convert_alpha()
        self.player_bank_right_image = pygame.image.load(
            path.join(self.img_folder, "player_ship_1_gun_bank_right.png")).convert_alpha()
        self.player_bank_left_image = pygame.image.load(
            path.join(self.img_folder, "player_ship_1_gun_bank_left.png")).convert_alpha()

        temp_image = pygame.image.load(path.join(self.img_folder, "player_shot.png")).convert_alpha()
        temp_rect = temp_image.get_rect()
        self.player_bullet_image = pygame.transform.scale(temp_image, (temp_rect.width // 6, temp_rect.height // 6))

        temp_image = pygame.image.load(path.join(self.img_folder, "drone.png")).convert_alpha()
        temp_rect = temp_image.get_rect()
        temp_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
        self.enemy_image = pygame.transform.rotate(temp_image, 180)

        temp_image = pygame.image.load(path.join(self.img_folder, "enemy_stationery_laser.png")).convert_alpha()
        self.ground_enemy_image_left = temp_image
        self.ground_enemy_image_right = pygame.transform.flip(temp_image, True, False)

        # SPRITESHEETS FOR ANIMATIONS BELOW
        self.asteroid_spritesheet = sprites.Spritesheet(path.join(self.img_folder, "asteroid_medium_spritesheet.png"))
        self.asteroid_frames_large = []
        self.asteroid_frames_medium = []
        self.asteroid_frames_small = []
        for i in range(8):
            temp_image = self.asteroid_spritesheet.get_image(120 * i, 0, 120, 120)
            temp_rect = temp_image.get_rect()
            temp_image.set_colorkey(settings.BLACK)
            self.asteroid_frames_large.append(temp_image)
            temp_image = pygame.transform.scale(temp_image, (temp_rect.width // 2, temp_rect.height // 2))
            self.asteroid_frames_medium.append(temp_image)
            temp_image = pygame.transform.scale(temp_image, (temp_rect.width // 4, temp_rect.height // 4))
            self.asteroid_frames_small.append(temp_image)

        self.explosion_spritesheet = sprites.Spritesheet(path.join(self.img_folder, "explosion.png"))
        self.explosion_frames = []
        for i in range(8):
            temp_image = self.explosion_spritesheet.get_image(763 * i, 0, 763, 751, 4)
            temp_rect = temp_image.get_rect()
            temp_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
            temp_image.set_colorkey(settings.BLACK)
            self.explosion_frames.append(temp_image)

        self.death_explosion_spritesheet = sprites.Spritesheet(path.join(self.img_folder, "death_explosion.png"))
        self.death_explosion_frames = []
        for i in range(8):
            temp_image = self.death_explosion_spritesheet.get_image(938 * i, 0, 938, 800)
            temp_rect = temp_image.get_rect()
            temp_image = pygame.transform.scale(temp_image, (temp_rect.width // 8, temp_rect.height // 8))
            temp_image.set_colorkey(settings.BLACK)
            self.death_explosion_frames.append(temp_image)

    def update(self):
        if self.machine.state == 'start screen':
            self.update_start_screen()
        elif self.machine.state == 'playing':
            self.update_playing_state()

    def update_start_screen(self):
        for button in self.buttons:
            button.update(self.mouse)

    def update_playing_state(self):
        # Update all of the sprite groups
        self.player_sprite.update()
        self.enemies.update()
        self.asteroids.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.explosions.update()
        self.background_stars.update()

        now = pygame.time.get_ticks()

        # creates background stars
        if now - self.star_update > 200:
            self.star_update = now
            sprites.Star(self)

        # update the level
        self.level_one.update_level()

        # Detect if the player's bullets hit any enemy ships
        hits = pygame.sprite.groupcollide(self.enemies, self.player_bullets, False, True)
        for hit in hits:
            for bullet in hits[hit]:
                hit.current_hull -= 25
                if hit.current_hull <= 0:
                    hit.kill()
            explosion_animation = sprites.SingleAnimation(hit.rect.center, self.explosion_frames, 50)
            self.explosions.add(explosion_animation)

        # Detect if the player's bullets hit any asteroids
        # When asteroids are destroyed they break into 2 asteroids of the next smaller size
        hits = pygame.sprite.groupcollide(self.asteroids, self.player_bullets, False, True)
        for hit in hits:
            for bullet in hits[hit]:
                hit.current_hull -= 25
                if hit.current_hull <= 0:
                    hit.kill()
                    if hit.size == 'large':
                        enemies.Asteroid(self, 'medium', True, hit.rect)
                        enemies.Asteroid(self, 'medium', True, hit.rect)
                    if hit.size == 'medium':
                        enemies.Asteroid(self, 'small', True, hit.rect)
                        enemies.Asteroid(self, 'small', True, hit.rect)
            explosion_animation = sprites.SingleAnimation(hit.rect.center, self.explosion_frames, 50)
            self.explosions.add(explosion_animation)

        # Detect if the player collides with any enemy ships or asteroids or enemy bullets
        # Player unable to be hurt/collide for a period of time after taking damage
        if not self.player.invulnerable:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(enemy, self.player):
                    self.player.enemy_collision()
            for asteroid in self.asteroids:
                if pygame.sprite.collide_mask(asteroid, self.player):
                    self.player.enemy_collision()
            for bullet in self.enemy_bullets:
                if pygame.sprite.collide_mask(bullet, self.player):
                    self.player.enemy_collision()

    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # ALL KEYDOWN and KEYUP EVENTS HERE
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

                # PASS THROUGH TO A CONTROLLER
                self.player.keyboard_button(event)

                # Escape currently exits the game
                # change to a pause type of screen eventually
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

            # ALL JOYBUTTON DOWN AND UP EVENTS HERE
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:

                # PASS THROUGH TO A CONTROLLER
                self.player.joystick_button(event)

    def draw(self):
        # START NEW FRAME
        self.screen.fill(settings.BLACK)

        # Call methods to draw depending on the game state
        if self.machine.state == 'start screen':
            self.draw_start_screen()
        elif self.machine.state == 'playing':
            self.draw_playing_state()

        # DISPLAY FRAME
        pygame.display.flip()

    def draw_start_screen(self):
        self.draw_text(settings.TITLE, 150, settings.YELLOW, settings.WIDTH / 2, settings.HEIGHT / 8, True)

        for button in self.buttons:
            button.draw(self.screen)
            if button.text is not None:
                self.draw_text(button.text, 50, settings.WHITE, button.rect.centerx,
                                    button.rect.top + button.rect.height / 6, True)

    def draw_playing_state(self):
        # DRAW ALL SPRITE GROUPS
        self.background_stars.draw(self.screen)
        self.enemies.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.explosions.draw(self.screen)

        # UI / HUD stuff, probably move to a function later
        self.draw_bar(10, 10, self.player.current_hull / self.player.max_hull, settings.RED)
        if self.player.max_shield > 0:
            self.draw_bar(10, 30, self.player.current_shield / self.player.max_shield, settings.BLUE)




    # GENERIC METHOD TO DRAW TEXT - CONSIDER MOVING TO A UI FILE WITH BUTTONS
    def draw_text(self, text, size, color, x, y, centered):
        font = pygame.font.Font(settings.FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        if centered:
            text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    # GENERIC METHOD TO DRAW A FILLED IN BAR WITH A WHITE OUTLINE
    def draw_bar(self, x, y, percentage, color):
        if percentage < 0:
            percentage = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        filled = percentage * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pygame.Rect(x, y, filled, BAR_HEIGHT)
        pygame.draw.rect(self.screen, settings.BLACK, outline_rect)
        pygame.draw.rect(self.screen, color, filled_rect)
        pygame.draw.rect(self.screen, settings.WHITE, outline_rect, 2)