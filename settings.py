import pygame
pygame.init()

# define colors
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GREY   = (128, 128, 128)
RED    = (255,   0,   0)
ORANGE = (255, 165,   0)
YELLOW = (255, 255,   0)
GREEN  = (  0, 128,   0)
BLUE   = (  0,   0, 255)
PURPLE = (128,   0, 128)
BROWN  = (165,  42,  42)

# Joystick Buttons
JOYBUTTONS = {
            'A'           : 0,
            'B'           : 1,
            'X'           : 2,
            'Y'           : 3,
            'LeftBumper'  : 4,
            'RightBumper' : 5,
            'Back'        : 6,
            'Start'       : 7,
            'LeftStick'   : 8,
            'RightStick'  : 9
           }

JOYAXIS = {
    'LeftHorizontal' : 0,
    'LeftVertical'   : 1,
    'Trigger'        : 2,               # Positive 1 is Left Down, Negative 1 is Right Down
    'RightHorizontal': 3,
    'RightVertical'  : 4
}

# game settings
DISPLAY_INFO = pygame.display.Info()
WIDTH = DISPLAY_INFO.current_w
HEIGHT = DISPLAY_INFO.current_h
FPS = 60
TITLE = 'Top-Down Shooter'
FONT = pygame.font.match_font('courier')

# SHIP SETTINGS
PLAYER_SHIP_1 = {
    'hull': 100,
    'shield': 0,
    'thrust': 1,
    'banking': 1,
    'weapon slots': 1
}

PLAYER_SHIP_2 = {
    'hull': 100,
    'shield': 100,
    'thrust': 2,
    'banking': 2,
    'weapon slots': 2
}

PLAYER_SHIP_3 = {
    'hull': 200,
    'shield': 100,
    'thrust': 3,
    'banking': 3,
    'weapon slots': 3
}