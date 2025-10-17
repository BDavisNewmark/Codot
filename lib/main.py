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
space.add(player1.body, player1.shape, player1.center, player1.motor)
# player1.body.apply_impulse_at_local_point((600, -1000), (0, 0))

static = [
    pymunk.Segment(space.static_body, (0, 720), (1280, 720), 10)
]

for s in static:
    s.friction = floor_friction

space.add(*static)


while running:
    space.step(1 / 60)
    clock.tick(60)
    screen.fill("white")

    player1.motor.activate_bodies()

    m = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                m = True
                player1.move(1)
                print("a")
            elif event.key == pygame.K_d:
                m = True
                player1.move(-1)
                print("d")
            elif event.key == pygame.K_w:
                player1.hold(True)
                print("w")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player1.move(0)
                print("-a")
            elif event.key == pygame.K_d:
                player1.move(0)
                print("-d")
            elif event.key == pygame.K_w:
                player1.hold(False)
                print("-w")

    print(player1.motor.impulse)
        

    space.debug_draw(draw_options)
    pygame.display.flip()