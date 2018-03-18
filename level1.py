import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from ShadowCapture import ShadowCapture
from ShadowNode import ShadowNode
from VectorShadowCapture import VectorShadowCapture
from pymunk import Vec2d
def inRegion(region,body):
    x,y = body.position
    if x >= region[0] and y <= region[1] and x <= region[2] and y >= region[3]:
        return True
    else:
        return False

def main():
    shadowCapture = VectorShadowCapture()
    pygame.init()
    screen = pygame.display.set_mode([1280, 960])
    pygame.display.set_caption("Shadow Caster Level 2")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    PLAYER_VELOCITY = 300. *2.
    space = pymunk.Space(threaded=True)
    space.gravity = (0.0, -1500.0)
    static = [pymunk.Segment(space.static_body, (0,0), (1280,0), 3),
                            pymunk.Segment(space.static_body, (1280,0), (1280,960), 3),
                            pymunk.Segment(space.static_body, (1280,960), (0,960), 3),
                            pymunk.Segment(space.static_body, (0,960), (0,0), 3)
                ]
    for segment in static:
        segment.friction = 1.
        space.add(segment)
    mass = 1
    radius = 60
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = 90,900
    objective = pymunk.Circle(body,radius, (0,0))
    objective.elasticity = .5
    objective.friction = 1
    space.add(body, objective)
    objectiveRegion = [1180,100,1280,0]
    segment = pymunk.Segment(space.static_body,(1180,100),(1280,0),3)
    # space.add(segment)
    finished = False
    while not finished:
        finished = inRegion(objectiveRegion,objective.body)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shadowCapture.resetBackground()
        surface = shadowCapture.update(space) # Update the space with what's captured in the camera. Return a pygame image of the silhouette.
        screen.fill((255,255,255))
        pygame.draw.circle(surface, (255,0,0), (1210,890), 70, 3)
        screen.blit(surface, surface.get_rect())
        space.debug_draw(draw_options)
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)
    screen.fill((225,255,255))

    font = pygame.font.SysFont("Arial", 32)
    screen.blit(font.render("Level 1 Complete! Esc to close window", 1, (0,0,0)), (480,480))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

if __name__ == '__main__':
    main()
