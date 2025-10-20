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

player2 = player(500, 100, ("red_player.png", "red_player_hold.png"))
space.add(player2.body, player2.shape, player2.center, player2.motor)

rod = pymunk.PinJoint(player1.body, player2.body, (0, 0), (0, 0))
space.add(rod)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    m = 0
    if keys[pygame.K_a]: m += 1
    if keys[pygame.K_d]: m -= 1
    if keys[pygame.K_w]:
        j = player1.hold(True)
        if j is not None: space.add(*j)
    else:
        j = player1.hold(False)
        if j is not None:
            space.remove(*j)
            for x in j: del x
    if player1.holding:
        relative = player1.body.position.get_angle_degrees_between(player2.body.position)
        relative += 90 if m == 1 else -90 if m == -1 else 0
        force = pymunk.Vec2d.from_polar(player_push, relative)
        player2.body.apply_force_at_world_point(force, player1.body.position)
    else: player1.move(m)

    m = 0
    if keys[pygame.K_LEFT]: m += 1
    if keys[pygame.K_RIGHT]: m -= 1
    if keys[pygame.K_UP]:
        j = player2.hold(True)
        if j is not None: space.add(*j)
    else:
        j = player2.hold(False)
        if j is not None:
            space.remove(*j)
            for x in j: del x
    if player2.holding:
        relative = player2.body.position.get_angle_degrees_between(player1.body.position)
        relative += 90 if m == 1 else -90 if m == -1 else 0
        force = pymunk.Vec2d.from_polar(player_push, relative)
        player1.body.apply_force_at_world_point(force, player2.body.position)
    else: player2.move(m)
    

    space.debug_draw(draw_options)
    pygame.display.flip()