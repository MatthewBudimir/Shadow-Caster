import numpy as np
import cv2
import pygame
import pymunk
from pymunk import Vec2d, BB
import pymunk.pygame_util
import pymunk.autogeometry
# https://stackoverflow.com/questions/34364678/how-to-get-foreground-mask-given-background-image Props to this guy
def getForegroundMask(frame, background, th):
    # reduce the noise in the frame
    frame = cv2.blur(frame, (5,5))
    # get the absolute difference between the foreground and the background
    fgmask= cv2.absdiff(frame, background)
    # convert foreground mask to gray
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
    # apply threshold (th) on the foreground mask
    _, fgmask = cv2.threshold(fgmask, th, 255, cv2.THRESH_BINARY)
    # setting up a kernal for morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # apply morpholoygy on the foreground mask to get a better result
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    return fgmask

class VectorShadowCapture:
    def resetBackground(self):
        ret,self.background = self.cap.read()
        self.background = cv2.flip(self.background,3)
        self.background = cv2.blur(self.background,(5,5))
        # cv2.imwrite("sample.png",self.background)
    def __init__(self):
        # Get a camera, take a picture of our background
        self.cap = cv2.VideoCapture(0)
        # Camera has completely blank image for first few inputs. Flush that out by reading the camera a few times.
        for i in range(32):
            self.cap.read()
        # Set the background image
        self.resetBackground()
        #Update always returns a 128x96 bitmap at the moment.
    def cvimage_to_pygame(self,image):
        image = cv2.flip(image,0)
        image = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
        return pygame.image.frombuffer(image.tostring(), [1280,960],"RGB")
    def cvimage_to_background(self,image):
        image = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        image = cv2.bitwise_not(image)
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
        return pygame.image.frombuffer(image.tostring(), [1280,960],"RGB")

    # Courtesy of Deformable.py from pymunk examples
    def generate_geometry(self,surface, space):
        for s in space.shapes:
            if hasattr(s, "generated") and s.generated:
                space.remove(s)

        def sample_func(point):
            try:
                p = int(point.x), int(point.y)
                color = surface.get_at(p)
                return color.hsla[2] # use lightness
            except:
                return 0

        line_set = pymunk.autogeometry.PolylineSet()
        def segment_func(v0, v1):
            line_set.collect_segment(v0, v1)

        pymunk.autogeometry.march_soft(BB(0,0,1280,960), 60, 60, 80, segment_func, sample_func)
        filter = pymunk.ShapeFilter(categories=0x2)
        for polyline in line_set:
            line = pymunk.autogeometry.simplify_curves(polyline, 1.)
            for i in range(len(line)-1):
                p1 = line[i]
                p2 = line[i+1]
                shape = pymunk.Segment(space.static_body, p1, p2, 5)
                shape.friction = 1
                shape.elasticity =1
                shape.color = pygame.color.THECOLORS["black"]
                shape.filter = filter
                shape.generated = True
                space.add(shape)
    def update(self,space):
        # arbitrary threshold value
        # Only works with 640x480 cameras
        print("Updating")
        threshold = 10
        # Blur the image to reduce noise
        ret,frame = self.cap.read()
        frame = cv2.flip(frame,3)
        foreground = cv2.blur(frame,(5,5))
        self.mask = getForegroundMask(frame,self.background,threshold)
        surface = self.cvimage_to_pygame(self.mask)
        self.generate_geometry(surface,space)
        return self.cvimage_to_background(self.mask)

    def updateWithBlocking(self,space,region):
        # arbitrary threshold value
        # Only works with 640x480 cameras
        print("Updating")
        threshold = 10
        # Blur the image to reduce noise
        ret,frame = self.cap.read()
        frame = cv2.flip(frame,3)
        foreground = cv2.blur(frame,(5,5))
        self.mask = getForegroundMask(frame,self.background,threshold)
        # Draw region on top of mask
        pts = np.array(region, np.int32)
        self.mask = cv2.fillConvexPoly(self.mask,pts,(0))
        surface = self.cvimage_to_pygame(self.mask)
        self.generate_geometry(surface,space)
        return self.cvimage_to_background(self.mask)


    def save(self):
        bitmap = np.zeros((96,128),np.uint8)
        for x in range(0,640,5):
            for y in range(0,480,5):
                if cv2.countNonZero(self.mask[y:y+5,x:x+5]) > 5:
                    m1 = int(y/5)
                    m2 = int(x/5)
                    bitmap[m1,m2]=1;
        display = np.zeros((480,640,3), np.uint8)
        for x in range(0,128):
            for y in range(0,96):
                if bitmap[y,x] > 0:
                    display[y*5:y*5+5,x*5:x*5+5] = 255
        cv2.imwrite("sample.png",display)
    def close(self):
        self.cap.release()
