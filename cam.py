import pygame
import pygame.transform
import pygame.camera
from pygame.locals import *
import sys
import time

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'

def surfdiff(current,original):
    if (current.get_width() != original.get_width()) or (current.get_height() != original.get_height()):
        sys.exit()
    height = current.get_height()
    width = current.get_width()
    for x in range(0,width):
        for y in range(0,height):
            curr = current.get_at([x,y])
            orig = original.get_at([x,y])
            # significant = False #Significant if difference is large enough
            # for i in range(4):
            #     if abs(curr[i]-orig[i]) > 20:
            #         significant = True
            #         #print("ding")
            #         break
            # if significant == True:
            #     current.set_at([x,y],[0,255,0,255])
            total = 0
            for i in range(4):
                total = total + abs(curr[i]-orig[i])
            if total > 30:
                current.set_at([x,y],[0,255,0,255])
            else:
                current.set_at([x,y],[0,0,0,255])
    return current

def valid(x):
    if x < 0:
        return 0
    elif x>255:
        return 255
    else:
        return x
def averagepix(surf):
    total = [0,0,0,0]
    for x in range(0,surf.get_width()):
      for y in range(0,surf.get_height()):
          total = list(map(lambda i,j: i+j,total,surf.get_at([x,y])))
    total = list(map(lambda i: i/(x*y),total))
    return total
def camstream():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode((1280, 960), 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    time.sleep(1)
    initial = camera.get_image(screen).copy()
    height = initial.get_height()
    width = initial.get_width()
    print(height)
    print(width)
    print(initial.get_at([0,0]))
    print(averagepix(initial))
    while capture:
        initial = camera.get_image(screen).copy()
        screen = camera.get_image(screen)
        screen = surfdiff(screen,initial)
        derr = pygame.transform.scale2x(pygame.transform.flip(screen.copy(),True,False))
        display.blit(derr,(5,5))
        pygame.display.flip()
        #pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_s:
                pygame.image.save(screen, FILENAME)
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
