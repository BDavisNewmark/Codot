import pygame
import pymunk
from pymunk import pygame_util
from classes import *
from constants import *
import map
from math import pi

pygame.init()
try: pygame.mixer.init()
except pygame.error: sound = False
else: sound = True



def init(window: pygame.Surface, scalar: float, level: int):
    global screen, scale, space, clock, draw_options, player1, player2, hbody, ibody, dim, gp, levelnum, flag
    screen = window
    scale = scalar
    levelnum = level
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = 0, gravity
    draw_options = pygame_util.DrawOptions(screen)
    hbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    ibody = pymunk.Body(body_type = pymunk.Body.STATIC)
    space.add(hbody, ibody)
    dim, p1p, p2p, gp = map.load(level, space, hbody, ibody) # type: ignore

    player1 = player(p1p[0], p1p[1], ("blue_player.png", "blue_player_hold.png"))
    space.add(player1.body, player1.shape, player1.center, player1.motor)
    
    player2 = player(p2p[0], p2p[1], ("red_player.png", "red_player_hold.png"))
    space.add(player2.body, player2.shape, player2.center, player2.motor)
    
    rod = pymunk.PinJoint(player1.body, player2.body, (0, 0), (0, 0))
    rod.error_bias = 0.1 ** 60
    space.add(rod)

    flag = pymunk.BB.newForCircle(gp, flag_size / 2)



def collide(a: pymunk.Arbiter, file: str):
    if a.is_first_contact and (a.bodies[0].id == player1.body.id or a.bodies[1].id == player1.body.id or a.bodies[0].id == player2.body.id or a.bodies[1].id == player2.body.id) and sound: pygame.mixer.Sound(f"./sounds/{file}.mp3").play()



def step() -> bool:
    global screen, space, clock, draw_options, player1, player2, hbody
    
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
        player1.move(0, player2)
        if m != 0:
            mangle = player1 - player2
            mangle += m * pi / 2
            mangle %= 2 * pi
            force = (cos(mangle) * player_push, sin(mangle) * player_push)
            player2.body.apply_force_at_world_point(force, player2.body.position)
    else: player1.move(m, player2)

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
        player2.move(0, player1)
        if n != 0:
            nangle = player2 - player1
            nangle += n * pi / 2
            nangle %= 2 * pi
            force = (cos(nangle) * player_push, sin(nangle) * player_push)
            player1.body.apply_force_at_world_point(force, player1.body.position)
    else: player2.move(n, player1)

    space.static_body.each_arbiter(lambda a : collide(a, "ground"))
    hbody.each_arbiter(lambda a : collide(a, "sticky"))
    ibody.each_arbiter(lambda a : collide(a, "icy"))

    if player1.bb.intersects(flag) or player2.bb.intersects(flag): return True
    else: return False

    # space.debug_draw(draw_options)
    # pygame.display.flip()