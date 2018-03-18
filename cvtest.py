# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2(50,50)
# # fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
#
# ############### SUBTRACTED EDGES AND EDGE DETECTION ####################
# while(1):
#     ret, frame = cap.read()
#     frame = cv2.flip(frame,1)
#     #Edge detection
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     lower_red = np.array([30,150,50])
#     upper_red = np.array([255,255,180])
#     mask = cv2.inRange(hsv, lower_red, upper_red)
#     res = cv2.bitwise_and(frame,frame, mask= mask)
#     edges = cv2.Canny(frame,100,100)
#     #Background subtraction to ignore background edges
#     fgmask = fgbg.apply(edges)
#     # fgmask = cv2.GaussianBlur(fgmask,(5,5),0)
#     fgmask = cv2.resize(fgmask, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
#     cv2.imshow('ORIGINAL',frame)
#     cv2.imshow('COMPLETE',fgmask)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#     if cv2.waitKey(30) == ord(' '):
#         print("Saving")
#         cv2.imwrite("sample.png",fgmask)
#         cv2.imwrite("source.png",frame)
#
# cap.release()
# cv2.destroyAllWindows()

# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
# # fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
#
# ############### EDGE DETECTION ONLY ####################
# while(1):
#     ret, frame = cap.read()
#     frame = cv2.flip(frame,1)
#     #Edge detection
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     lower_red = np.array([30,150,50])
#     upper_red = np.array([255,255,180])
#     mask = cv2.inRange(hsv, lower_red, upper_red)
#     res = cv2.bitwise_and(frame,frame, mask= mask)
#     edges = cv2.Canny(frame,125,125)
#     # fgmask = edges
#     # for x in range(0,640,10):
#     #     for y in range(0,480,10):
#     #         #Calculate the total amount of "white" in a 10x10 area starting at y,x
#     #         # fgmask[y,x] = (255)
#     #         # count the number of non black pixels
#     #         if cv2.countNonZero(fgmask[y:y+10,x:x+10]) > 5:
#     #             fgmask[y:y+10,x:x+10] = 255
#     fgmask = cv2.resize(edges, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
#
#     cv2.imshow('COMPLETE',fgmask)
#     cv2.imshow('ORIGINAL',frame)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#     if cv2.waitKey(30) == ord(' '):
#         print("Saving")
#         cv2.imwrite("sample.png",fgmask)
#         cv2.imwrite("source.png",frame)
#
# cap.release()
# cv2.destroyAllWindows()

###### PSUDO MOTION DETECTOR ##########
# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2(2,100)
# # fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# while(1):
#     ret, frame = cap.read()
#     # frame = cv2.resize(frame, None, fx = 0.7, fy = 0.7, interpolation = cv2.INTER_CUBIC)
#     frame = cv2.flip(frame,3)
#     fgmask = fgbg.apply(frame)
#     # fgmask = cv2.threshold(fgmask,127,255,cv2.THRESH_BINARY)
#     # ret2,fgmask = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY)
#     fgmask = cv2.resize(fgmask, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
#     cv2.imshow('cam',frame)
#     cv2.imshow('silhouette',fgmask)
#
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
#
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np
# cap = cv2.VideoCapture(0)
# kernel = np.ones((3,3),np.float32) * (-1)
# kernel[1,1] = 8
# for i in range(300):
#     ret,frame = cap.read()
#     cv2.imshow('cam',frame)
# while(1):
#     ret,frame = cap.read()
#     dst = cv2.filter2D(frame,-1,kernel)
#     cv2.imshow('cam',dst)
# cap.release()
# cv2.destroyAllWindows()

#### PSUDO GREEN SCREEN ##########
# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2(500,20)
# ret,frame = cap.read()
# height, width, channels = frame.shape
# # fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# fgmask = 0;
# #threshold
# thresh = 50;
# gridsize = 10;
# bitmap = np.zeros((96,128),np.uint8)
# while(1):
#     ret, frame = cap.read()
#     # frame = cv2.resize(frame, None, fx = 0.7, fy = 0.7, interpolation = cv2.INTER_CUBIC)
#     frame = cv2.flip(frame,3)
#     fgmask = fgbg.apply(frame)
#     # fgmask = cv2.threshold(fgmask,127,255,cv2.THRESH_BINARY)
#     # ret2,fgmask = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY)
#     # For every grid box
#
#     # bitmap = np.zeros((96,128),np.uint8)
#     # changemap = np.zeros((96,128),np.uint8)
#     bitmap = np.zeros((96,128),np.uint8)
#     for x in range(0,640,5):
#         for y in range(0,480,5):
#             #Calculate the total amount of "white" in a 10x10 area starting at y,x
#             # fgmask[y,x] = (255)
#             # count the number of non black pixels
#             if cv2.countNonZero(fgmask[y:y+5,x:x+5]) > 5:
#                 m1 = int(y/5)
#                 m2 = int(x/5)
#                 bitmap[m1,m2]=5;
#
#     # fgmask = cv2.resize(fgmask, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
#     # # PIXEL AGING
#     # for x in range(0,128):
#     #     for y in range(0,96):
#     #         if bitmap[y,x] >0:
#     #             bitmap[y,x] -=1
#
#     # # AREA CLEARING
#     # for x in range(1,127):
#     #     for y in range(1,96):
#     #         if changemap[y,x] == 1:
#     #             bitmap[x-3:x+3,y-3:y+3] = 0;
#     # for x in range(0,128):
#     #     for y in range(0,96):
#     #         if changemap[y,x] == 1:
#     #             bitmap[y,x] =1
#     display = np.zeros((480,640,3), np.uint8)
#     for x in range(0,128):
#         for y in range(0,96):
#             if bitmap[y,x] > 0:
#                 display[y*5:y*5+5,x*5:x*5+5] = 255
#     cv2.imshow('cam',frame)
#     cv2.imshow('motion',fgmask)
#     cv2.imshow('processed',display)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#     if k == 32:
#         bitmap = np.zeros((96,128),np.uint8)
#
# cap.release()
# cv2.destroyAllWindows()

#### FAKE GREENSCREEN: REQUIRES AUTO EXPOSURE DISABLED
# import numpy as np
# import cv2
#
# def getForegroundMask(frame, background, th):
#     # reduce the nois in the farme
#     frame = cv2.blur(frame, (5,5))
#     # get the absolute difference between the foreground and the background
#     fgmask= cv2.absdiff(frame, background)
#     # convert foreground mask to gray
#     fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
#     # apply threshold (th) on the foreground mask
#     _, fgmask = cv2.threshold(fgmask, th, 255, cv2.THRESH_BINARY)
#     # setting up a kernal for morphology
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#     # apply morpholoygy on the foreground mask to get a better result
#     fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
#     return fgmask
#
# cap = cv2.VideoCapture(0)
# ret,background = cap.read()
# background = cv2.flip(background,3)
# background = cv2.blur(background,(5,5))
# # avg1 = np.float32(background)
# while(1):
#     ret, frame = cap.read()
#     frame = cv2.flip(frame,3)
#     foreground = cv2.blur(frame,(5,5))
#     # frame = foreground
#     # cv2.accumulateWeighted(frame,avg1,0.01)
#     # res1 = cv2.convertScaleAbs(avg1)
#
#     # mask = getForegroundMask(frame,res1,5)
#     mask = getForegroundMask(frame,background,5)
#     cv2.imshow('cam',frame)
#     cv2.imshow('mask',mask)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#     if k == 32:
#         ret,background = cap.read()
#         background = cv2.flip(background,3)
#         background = cv2.blur(background,(5,5))
#
# cap.release()
# cv2.destroyAllWindows()

#### FAKE GREENSCREEN: WITH PIXELLING
import numpy as np
import cv2
def getForegroundMask(frame, background, th):
    # reduce the nois in the farme
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

cap = cv2.VideoCapture(0)
for i in range(32):
    cap.read()
ret,background = cap.read()
background = cv2.flip(background,3)
background = cv2.blur(background,(5,5))
# avg1 = np.float32(background)
while(1):
    ret, frame = cap.read()
    frame = cv2.flip(frame,3)
    foreground = cv2.blur(frame,(5,5))
    # frame = foreground
    # cv2.accumulateWeighted(frame,avg1,0.01)
    # res1 = cv2.convertScaleAbs(avg1)

    # mask = getForegroundMask(frame,res1,5)
    mask = getForegroundMask(frame,background,10)
    bitmap = np.zeros((96,128),np.uint8)
    for x in range(0,640,5):
        for y in range(0,480,5):
            #Calculate the total amount of "white" in a 10x10 area starting at y,x
            # fgmask[y,x] = (255)
            # count the number of non black pixels
            if cv2.countNonZero(mask[y:y+5,x:x+5]) > 10:
                m1 = int(y/5)
                m2 = int(x/5)
                bitmap[m1,m2]=1;
    display = np.zeros((480,640,3), np.uint8)
    for x in range(0,128):
        for y in range(0,96):
            if bitmap[y,x] > 0:
                display[y*5:y*5+5,x*5:x*5+5] = 255
    # display = cv2.bitwise_not(display)
    stuff =  [[320,0],[100,480],[400,480]]#[[0,0],[100,0],[100,100],[0,100]]
    pts = np.array(stuff, np.int32)
    mask = cv2.fillConvexPoly(mask,pts,(0,0,0))
    cv2.imshow('cam',frame)
    cv2.imshow('mask',mask)
    # cv2.imshow('pixels',display)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    if k == 32:
        ret,background = cap.read()
        background = cv2.flip(background,3)
        background = cv2.blur(background,(5,5))

cap.release()
cv2.destroyAllWindows()
