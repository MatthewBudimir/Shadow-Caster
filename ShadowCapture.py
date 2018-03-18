import numpy as np
import cv2
# https://stackoverflow.com/questions/34364678/how-to-get-foreground-mask-given-background-image Props to this guy
def getForegroundMask(frame, background, th):
    # reduce the noise in the farme
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

class ShadowCapture:
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
    def update(self):
        # arbitrary threshold value
        # Only works with 640x480 cameras
        print("Updating")
        threshold = 10
        ret,frame = self.cap.read()
        frame = cv2.flip(frame,3)
        foreground = cv2.blur(frame,(5,5))
        self.mask = getForegroundMask(frame,self.background,threshold)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([30,150,50])
        upper_red = np.array([255,255,180])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        self.mask = cv2.Canny(self.mask,100,100)

        bitmap = np.zeros((96,128),np.uint8)
        for x in range(0,640,5):
            for y in range(0,480,5):
                if cv2.countNonZero(self.mask[y:y+5,x:x+5]) > 2:
                    m1 = int(y/5)
                    m2 = int(x/5)
                    bitmap[m1,m2]=1;
        return bitmap
        # take a picture from the webcam return bitmap
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
