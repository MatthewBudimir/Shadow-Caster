import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
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

    #create pendulum
    mass = 1
    radius = 60
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = (440,430)
    body.start_position = Vec2d(body.position)
    objective = pymunk.Circle(body, radius)
    objective.elasticity = 0.75
    space.add(body, objective)
    pj = pymunk.PinJoint(space.static_body, body, (640,960), (0,0))
    space.add(pj)
    objectiveRegion = [1180,960,1280,860]
    finished = False
    forbiddenRegion = [[800,960],[1200,960],[1300,0],[700,0]]
    cvForbiddenRegion = [[500,-100],[250,480],[750,480]] # Using 640x480 image at this point
    while not finished:
        finished = inRegion(objectiveRegion,objective.body)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shadowCapture.resetBackground()
        surface = shadowCapture.updateWithBlocking(space,cvForbiddenRegion) # Update the space with what's captured in the camera. Return a pygame image of the silhouette.
        screen.fill((255,255,255))
        pygame.draw.polygon(surface, (93, 0, 166),[[1000,-100],[500,960],[1500,960]],0)
        pygame.draw.circle(surface, (255,0,0), (1210,70), 70, 3)
        screen.blit(surface, surface.get_rect())
        space.debug_draw(draw_options)
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)

    #Final screen
    screen.fill((225,255,255))
    font = pygame.font.SysFont("Arial", 32)
    screen.blit(font.render("Level 2 Complete! Esc to close window", 1, (0,0,0)), (480,480))
    pygame.display.flip()
    #Wait for them to close the game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

if __name__ == '__main__':
    main()
