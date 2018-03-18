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
def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 5
    radius = 30
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(60,200)
    body.position = x, 930
    shape = pymunk.Circle(body,radius, (0,0))
    shape.elasticity = 0.5
    space.add(body, shape)
    return shape
def main():
    shadowCapture = VectorShadowCapture()
    pygame.init()
    screen = pygame.display.set_mode([1280, 960])
    pygame.display.set_caption("Shadow Caster Level 3")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space = pymunk.Space(threaded=True)
    space.gravity = (0.0, -1500.0)
    static = [pymunk.Segment(space.static_body, (200,0), (1280,0), 3),
                            pymunk.Segment(space.static_body, (1280,0), (1280,960), 3),
                            pymunk.Segment(space.static_body, (1280,960), (0,960), 3),
                            pymunk.Segment(space.static_body, (0,960), (0,0), 3)
                ]
    for segment in static:
        segment.friction = 1.
        space.add(segment)
    mass = 100

    inertia = pymunk.moment_for_segment(mass, (-200,0), (200,0), 1)
    bar = pymunk.Body(mass, inertia)
    bar.position = 640,240
    barShape = pymunk.Segment(bar,(-400,0), (400,0),10)
    scaleFilter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0x2)
    barShape.filter = scaleFilter
    space.add(bar,barShape)
    pj = pymunk.PinJoint(space.static_body, bar, (640,240), (0,0))
    space.add(pj)
    # create gate
    gate = pymunk.Body(1,pymunk.moment_for_segment(1,(0,0),(0,220),1))
    gate.position = 1040,240
    gateShape = pymunk.Segment(bar,(400,0),(400,-240),10)
    gateShape.filter = scaleFilter
    boxLeft = [pymunk.Segment(bar, (-400,0), (-400,100), 3),pymunk.Segment(bar, (-100,0), (-100,100), 3)]
    boxRight = [pymunk.Segment(bar, (400,0), (400,100), 3),pymunk.Segment(bar, (100,0), (100,100), 3)]
    for segment in boxLeft + boxRight:
        segment.filter = scaleFilter
        segment.friction = 1.
        space.add(segment)

    counterweightMoment = pymunk.moment_for_circle(100,0,145,(0,0))
    counterweight = pymunk.Body(50,counterweightMoment)
    counterweightShape = pymunk.Poly(counterweight,[[0,0],[200,0],[200,100],[0,100]])
    counterweightShape.filter = scaleFilter
    counterweightShape.color = (255,0,0)
    counterweight.position = 744,240
    space.add(counterweightShape,counterweight)

    space.add(gate,gateShape)
    divider = pymunk.Segment(space.static_body,(640,0),(640,210),5)
    space.add(divider)
    # Create objective ball_shape
    mass = 1
    radius = 60
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = 700,70
    objective = pymunk.Circle(body,radius, (0,0))
    objective.elasticity = .5
    objective.friction = 1
    space.add(body, objective)
    objectiveRegion = [1180,100,1280,0]


    ticks_to_next_ball = 10
    finished = False
    balls = []
    while not finished:
        finished = inRegion(objectiveRegion,objective.body)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shadowCapture.resetBackground()
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)
        #remove irrelevant balls
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 0:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)
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
    screen.blit(font.render("Level 3 Complete! Esc to close window", 1, (0,0,0)), (480,480))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

if __name__ == '__main__':
    main()
