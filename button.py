import pygame
import settings


class Button:
    def __init__(self, game, x, y, width, height, text=None):
        self.game = game
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text

    def update(self, mouse):
        if self.is_hovering(mouse):
            self.image.fill(settings.RED)
        else:
            self.image.fill(settings.BLUE)
        if self.is_clicked(mouse):
            self.handle_event()

    def handle_event(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_hovering(self, mouse):
        mouse_pos = mouse.get_pos()
        if self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width and \
           self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height:
                return True
        else:
            return False

    def is_clicked(self, mouse):
        mouse_click = mouse.get_pressed()
        if mouse_click[0] and self.is_hovering(mouse):
            return True
        else:
            return False


class StartButton(Button):
    def handle_event(self):
        self.game.machine.new()


class ExitButton(Button):
    def handle_event(self):
        if self.game.playing:
            self.game.playing = False
        self.game.running = False

