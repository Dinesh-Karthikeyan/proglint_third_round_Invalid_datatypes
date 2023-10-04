import cv2
import numpy as np
# pts1 = np.array([[50,10],[200,50],[200,200],[50,200]], np.int32)
# pts1 = pts1.reshape((-1,1,2))


def coverShelfRegion(frame, pts, color=(0, 255, 255) ):
    cv2.fillPoly(frame,pts=[pts],color=color)
    