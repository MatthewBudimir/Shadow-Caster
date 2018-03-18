import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from ShadowCapture import ShadowCapture
from ShadowNode import ShadowNode
from VectorShadowCapture import VectorShadowCapture
from pymunk import Vec2d

def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(120,380)
    body.position = x, 550
    shape = pymunk.Circle(body,radius, (0,0))
    shape.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0x1 ^ 0x2)
    space.add(body, shape)
    return shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space(threaded=True)
    space.gravity = (0.0, -900.0)
    balls = []
    ###
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = 0,200
    shape = pymunk.Poly(body,([0,0],[0,10],[600,10],[600,0]))
    shape.filter = pymunk.ShapeFilter(categories=0x1)
    space.add(body, shape)

    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = 0,180
    shape = pymunk.Poly(body,([0,0],[0,10],[600,10],[600,0]))
    shape.filter = pymunk.ShapeFilter(categories=0x2)
    space.add(body, shape)

    ###
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                for line in lines:
                    space.remove(line)
                lines =[]

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill((255,255,255))

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 150:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.debug_draw(draw_options)

        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
