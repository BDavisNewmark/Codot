import pygame
import pymunk
from typing import *
from constants import *
pygame.init()



class player():
    def __init__(self, x: float, y: float, sprites: Tuple[str, str]):
        self.spriteN = pygame.image.load(f"./sprites/{sprites[0]}")
        self.spriteH = pygame.image.load(f"./sprites/{sprites[1]}")
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
                
                self.hpointb = pymunk.Body(body_type = pymunk.Body.STATIC)
                self.hpointb.position = self.body.position + (-10, 10)
                self.hpointb.shape = pymunk.Circle(self.hpointb, 1)
                self.hpointb.shape.collision_type = 0
                self.hjointb = pymunk.PinJoint(self.body, self.hpointb, (0, 0), (0, 0))
                self.hjointb.collide_bodies = False
                
                return (self.hpointa, self.hpointa.shape, self.hjointa, self.hpointb, self.hpointb.shape, self.hjointb)
                
            else:
                self.holding = False
                return (self.hjointa, self.hpointa.shape, self.hpointa, self.hjointb, self.hpointb.shape, self.hpointb)

    def move(self, direction: int):
        self.motor.rate = player_speed if direction == 1 else -player_speed if direction == -1 else 0