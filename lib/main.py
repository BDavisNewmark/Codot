import pygame
import pymunk
from pymunk import pygame_util
from classes import *
from constants import *

pygame.init()



screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
space = pymunk.Space()
space.gravity = 0, gravity

draw_options = pygame_util.DrawOptions(screen)


player1 = player(100, 100, ("blue_player.png", "blue_player_hold.png"))
space.add(player1.body, player1.shape)
# player1.body.apply_impulse_at_local_point((600, -1000), (0, 0))

while running:
    space.step(1 / 60)
    clock.tick(60)
    screen.fill("white")
    
    for event in pygame.event.get():
        ...

    space.debug_draw(draw_options)
    pygame.display.flip()