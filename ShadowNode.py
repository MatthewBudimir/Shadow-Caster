import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

class ShadowNode:
    def __init__(self,x,y,radius):
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = x,y
        self.shape = pymunk.Circle(self.body,radius,(0,0))
        self.active = False
    def update(self,nowActive,space):
        if self.active:
            if not nowActive:
                # print("deactivating")
                self.active = False
                space.remove(self.shape,self.shape.body)
        else:
            if nowActive:
                self.active = True
                # print("Activating")
                space.add(self.shape,self.shape.body)
