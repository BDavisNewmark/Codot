import pygame
import pymunk
from pymunk import pygame_util
from classes import *
from constants import *
from math import pi

pygame.init()



desksize = pygame.display.get_desktop_sizes()[0]
scale = min(desksize[0] / 1280, desksize[1] / 720)
scale = 1
screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
clock = pygame.time.Clock()
running = True
space = pymunk.Space()
space.gravity = 0, gravity

draw_options = pygame_util.DrawOptions(screen)


player1 = player(300, 100, ("blue_player.png", "blue_player_hold.png"))
space.add(player1.body, player1.shape, player1.center, player1.motor)

player2 = player(500, 100, ("red_player.png", "red_player_hold.png"))
space.add(player2.body, player2.shape, player2.center, player2.motor)

rod = pymunk.PinJoint(player1.body, player2.body, (0, 0), (0, 0))
rod.error_bias = 0.1 ** 60
space.add(rod)

hbody = pymunk.Body(body_type = pymunk.Body.STATIC)

static = [
    pymunk.Segment(space.static_body, (0, 720), (1280, 720), 10),
    pymunk.Segment(hbody, (1280, 0), (1280, 720), 10),
    pymunk.Segment(hbody, (0, 0), (0, 720), 10)
]

for x in static:
    x.friction = floor_friction

space.add(hbody, *static)


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
    if keys[pygame.K_w] and player1.holdable(hbody, space):
        j = player1.hold(True)
        if j is not None: space.add(*j)
    else:
        j = player1.hold(False)
        if j is not None:
            space.remove(*j)
            for x in j: del x
    if player1.holding:
        player1.move(0)
        if m != 0:
            mangle = player1 - player2
            mangle += m * pi / 2
            mangle %= 2 * pi
            force = (cos(mangle) * player_push, sin(mangle) * player_push)
            player2.body.apply_force_at_world_point(force, player2.body.position)
    else: player1.move(m)

    n = 0
    if keys[pygame.K_LEFT]: n += 1
    if keys[pygame.K_RIGHT]: n -= 1
    if keys[pygame.K_UP] and player2.holdable(hbody, space):
        j = player2.hold(True)
        if j is not None: space.add(*j)
    else:
        j = player2.hold(False)
        if j is not None:
            space.remove(*j)
            for x in j: del x
    if player2.holding:
        player2.move(0)
        if n != 0:
            nangle = player2 - player1
            nangle += n * pi / 2
            nangle %= 2 * pi
            force = (cos(nangle) * player_push, sin(nangle) * player_push)
            player1.body.apply_force_at_world_point(force, player1.body.position)
    else: player2.move(n)
    

    space.debug_draw(draw_options)
    pygame.display.flip()