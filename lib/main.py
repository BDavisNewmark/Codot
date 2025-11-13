import pygame
import level
import draw

while level.running:
    level.main()
    draw.draw()
    pygame.display.flip()