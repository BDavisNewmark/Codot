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
        self.holding = b
        if b:
            self.shape.friction = 99999
        else:
            self.shape.friction = player_friction

    def move(self, direction: int):
        self.motor.rate = player_speed if direction == 1 else -player_speed if direction == -1 else 0