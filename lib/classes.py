import pygame
import pymunk
from typing import *
from constants import *
from math import *
pygame.init()



class player():
    def __init__(self, x: float, y: float, sprites: Tuple[str, str]):
        self.spriteN = pygame.image.load(f"./sprites/player/{sprites[0]}")
        self.spriteH = pygame.image.load(f"./sprites/player/{sprites[1]}")
        self.holding = False
        self.sprite = lambda : self.spriteH if self.holding else self.spriteN
        
        self.body = pymunk.Body()
        self.body.position = x, y
        
        self.shape = pymunk.Circle(self.body, player_size)
        self.shape.mass = player_mass
        self.shape.friction = player_friction

        self.center = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.center.position = x, y
        self.center.shape = pymunk.Circle(self.center, 10)
        self.center.friction = center_friction
        
        self.motor = pymunk.SimpleMotor(self.center, self.body, 0)
        self.motor.collide_bodies = False

    
    def hold(self, b: bool):
        if self.holding != b:
            if b:
                self.holding = True
                
                self.hpointa = pymunk.Body(body_type = pymunk.Body.STATIC)
                self.hpointa.position = self.body.position + (10, 10)
                self.hpointa.shape = pymunk.Circle(self.hpointa, 1)
                self.hpointa.shape.collision_type = 0
                self.hjointa = pymunk.PinJoint(self.body, self.hpointa, (0, 0), (0, 0))
                self.hjointa.collide_bodies = False
                self.hjointa.max_force = nail_strength
                
                self.hpointb = pymunk.Body(body_type = pymunk.Body.STATIC)
                self.hpointb.position = self.body.position + (-10, 10)
                self.hpointb.shape = pymunk.Circle(self.hpointb, 1)
                self.hpointb.shape.collision_type = 0
                self.hjointb = pymunk.PinJoint(self.body, self.hpointb, (0, 0), (0, 0))
                self.hjointb.collide_bodies = False
                self.hjointb.max_force = nail_strength
                
                return (self.hpointa, self.hpointa.shape, self.hjointa, self.hpointb, self.hpointb.shape, self.hjointb)
                
            else:
                self.holding = False
                return (self.hjointa, self.hpointa.shape, self.hpointa, self.hjointb, self.hpointb.shape, self.hpointb)

    
    def move(self, direction: int, other: "player"):
        if self.holding and other.holding: self.motor.rate = 0
        else: self.motor.rate = player_speed if direction == 1 else -player_speed if direction == -1 else 0
            
            
    def __sub__(self, other: "player") -> float:
        ax, ay = self.body.position
        bx, by = other.body.position
        cx, cy = ax - bx, ay - by
        r = (cx ** 2 + cy ** 2) ** .5
        cx, cy = cx / r, cy / r
        return acos(cx) if cy > 0 else 2 * pi - acos(cx)

    
    def holdable(self, sticky: pymunk.Body, space: pymunk.Space) -> bool:
        can = False
        for x in space.shape_query(self.shape):
            if sticky is x.shape.body:
                can = True
                break
        return can

    
    def spriter(self, modify: float) -> pygame.Surface:
        image = self.sprite()
        image = pygame.transform.scale(image, (player_size * 2, player_size * 2))
        image = pygame.transform.rotate(image, -degrees(self.body.angle) - modify)
        return image

    
    def __add__(self, other: "player") -> float:
        ax, ay = self.body.position
        bx, by = other.body.position
        return sqrt((ax - bx) ** 2 + (ay - by) ** 2)



class Cursor():
    def __init__(self, sprites: str = "./sprites/gui/cursor/", size: Tuple[int, int] = mouse_size, angle: float = 135, point: Tuple[float, float] = (1/2, 1)):
        self.size = size
        self.angle = angle

        self.sprites = [
            pygame.image.load(f"{sprites}idle.png"),
            pygame.image.load(f"{sprites}hover.png"),
            pygame.image.load(f"{sprites}click.png")
        ]

        for i in range(3):
            x = pygame.transform.scale(self.sprites[i], size)
            x = pygame.transform.rotate(x, angle)
            self.sprites[i] = x

        """self.pointing = (
            (point[0]-(size[0]/2))*cos(radians(360-angle)) -
            (point[1]-(size[1]/2))*sin(radians(360-angle)) +
            max(abs((size[0]*cos(radians(360-angle))/2) -
            (size[1]*sin(radians(360-angle))/2)),
            abs((size[0]*cos(radians(360-angle))/2) -
            (size[1]*sin(radians(360-angle))/2))),
            (point[0]-(size[0]/2))*sin(radians(360-angle)) +
            (point[1]-(size[1]/2))*cos(radians(360-angle)) +
            max(abs((size[0]*sin(radians(360-angle))/2) -
            (size[1]*cos(radians(360-angle))/2)),
            abs((size[0]*sin(radians(360-angle))/2) -
            (size[1]*cos(radians(360-angle))/2)))
        )"""

        r = sqrt((size[0] / 2) ** 2 + (size[1] / 2) ** 2)
        x0, y0 = point[0] * size[0], point[1] * size[1]
        x1, y1 = (x0 - (size[0] / 2)) / r, (y0 - (size[1] / 2)) / r
        a = radians(360 - angle)
        c = complex(x1, y1) * complex(cos(a), sin(a))
        self.pointing = ((c.real * r) + (self.sprites[0].get_width() / 2), (c.imag * r) + (self.sprites[0].get_height() / 2))


    def hover(self, *objects: Callable[[Tuple[int, int]], bool]) -> int:
        pos = pygame.mouse.get_pos()
        out = -1
        for i, x in enumerate(objects):
            if x(pos):
                out = i
                break
        return out


    def draw(self, dim: Tuple[int, int], *objects: Callable[[Tuple[int, int]], bool]) -> pygame.Surface:
        hovered = self.hover(*objects)

        if pygame.mouse.get_pressed()[0]: sprite = self.sprites[2]
        elif hovered == -1: sprite = self.sprites[0]
        else: sprite = self.sprites[1]

        desksize = pygame.display.get_desktop_sizes()[0]
        scale = min(1, desksize[0] / 1280, desksize[1] / 720)
        pos = tuple(x / scale for x in pygame.mouse.get_pos())
        pos = (pos[0] - self.pointing[0], pos[1] - self.pointing[1])

        overlay = pygame.Surface(dim)
        overlay.fill("white")
        overlay.blit(sprite, pos)
        overlay.set_colorkey("white")
        
        return overlay