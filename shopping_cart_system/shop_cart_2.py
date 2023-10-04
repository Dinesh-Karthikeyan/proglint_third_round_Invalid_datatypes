import cv2
from object_detection_model import productDetection
from wrist_detection_model import wristDetection, wristDetectionNoCord
from shelf_region import coverShelfRegion
from cart_detect import cartDetection
import numpy as np
cap = cv2.VideoCapture(0)

pts1 = np.array([[50,10],[200,50],[200,200],[50,200]], np.int32)
pts1 = pts1.reshape((-1,1,2))
product = {"p1": 0}
pts2 = np.array([[200,300],[400,300],[400,400],[200,450]], np.int32)
pts2 = pts2.reshape((-1,1,2))

flag_shelf = False
flag_cart = False

def drawRec(top_left_cord, bottom_right_cord):
    cv2.rectangle(frame,top_left_cord, bottom_right_cord,(0,255,0),3)

def insideBox(pts, pixelCoord):
    result = cv2.pointPolygonTest(pts, pixelCoord, False) 
    return result

while cap.isOpened():
    success, frame = cap.read()
    if success:

        top_left_cord_rightHand, bottom_right_cord_rightHand, top_left_cord_leftHand, bottom_right_cord_leftHand, frame_rightHand, frame_leftHand, right_wrist_point, left_wrist_point = wristDetection(frame)
        drawRec(top_left_cord_rightHand,bottom_right_cord_rightHand)
        drawRec(top_left_cord_leftHand, bottom_right_cord_leftHand)
        
        res_right_hand_shelf = insideBox(pts1, right_wrist_point)
        if res_right_hand_shelf == 1:
            print("Shelf")
            flag_shelf = True

        try:
            if flag_shelf:
                detected_frame_right = productDetection(frame=frame_rightHand)
                if len(detected_frame_right) > 0:
                    product["p1"] = detected_frame_right
                    flag_shelf = False
                    flag_cart = True

        except(ZeroDivisionError):
            print(ZeroDivisionError)
        
        if flag_cart:
            res_right_hand_cart = insideBox(pts2, right_wrist_point)
            if res_right_hand_cart == 1:
                product["p1"] = "confirm"
                flag_cart = False

        print(product['p1'])
        coverShelfRegion(frame=frame,pts=pts1)

        coverShelfRegion(frame=frame, pts=pts2, color= (255, 255, 0))

        cv2.imshow("YOLOv8 Inference", frame) 

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break


cap.release()
cv2.destroyAllWindows()