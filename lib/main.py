import pygame
import level
import draw


level.init(0)
draw.init()

while level.running:
    level.step()
    draw.draw()
    pygame.display.flip()