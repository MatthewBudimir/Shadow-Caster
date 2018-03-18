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
    radius = 60
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(120,380)
    body.position = x, 550
    shape = pymunk.Circle(body,radius, (0,0))
    space.add(body, shape)
    return shape

def main():
    pygame.init()
    screen = pygame.display.set_mode([1280, 960])
    pygame.display.set_caption("ShadowGame")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space(threaded=True)
    space.gravity = (0.0, -1500.0)
    # Get the shadowCapture online for webcam usage
    shadowCapture = VectorShadowCapture()
    #create a pendulum
    mass = 10
    radius = 60
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, moment)
    body.position = (640,480)
    body.start_position = Vec2d(body.position)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9999999
    space.add(body, shape)
    pj = pymunk.PinJoint(space.static_body, body, (640,960), (0,0))
    space.add(pj)

    # run the simulation
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shadowCapture.resetBackground()
            elif event.type == KEYDOWN and event.key == K_m:
                shadowCapture.save()
        surface = shadowCapture.update(space) # Update the space with what's captured in the camera. Return a pygame image of the silhouette.
        screen.fill((255,255,255))
        screen.blit(surface, surface.get_rect())
        space.debug_draw(draw_options)
        space.step(1/50.0)
        print(len(space.shapes))
        pygame.display.flip()
        clock.tick(50)
        print("tick")
    # update the shadowNodes in the shadowMap based on whether the shadowMap deems they're active
    shadowCapture.close()
if __name__ == '__main__':
    main()
