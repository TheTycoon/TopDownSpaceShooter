import pygame
import game

app = game.Game()
app.new()
while app.running:
    app.run()

pygame.quit()


