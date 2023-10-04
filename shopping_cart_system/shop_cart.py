import cv2
from object_detection_model import productDetection
from wrist_detection_model import wristDetection, wristDetectionNoCord
from shelf_region import coverShelfRegion
from cart_detect import cartDetection
import numpy as np
cap = cv2.VideoCapture(0)

pts1 = np.array([[50,10],[200,50],[200,200],[50,200]], np.int32)
pts1 = pts1.reshape((-1,1,2))

pts2 = np.array([[200,300],[400,300],[400,400],[200,450]], np.int32)
pts2 = pts2.reshape((-1,1,2))

object_detected = False
object_detected_right = False
bill_entered = False
box_enter = False
box_enter_right = False
detected_object = 0

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
        
        res_right_hand = insideBox(pts1, right_wrist_point)
        res_left_hand = insideBox(pts1, left_wrist_point)

        try:
            # pass
            detected_frame_right = productDetection(frame=frame_rightHand)
            detected_frame_left = productDetection(frame=frame_leftHand)
            if detected_frame_left == []:
                object_detected = False
            if object_detected == False and (detected_frame_left != []):
                object_detected = True
                print("------------------------------------------------------------>>>>>")
                print(detected_frame_left)
                detected_object = detected_frame_left[0]
                print(detected_object)
                # break
            if object_detected == True and (res_left_hand == -1) and detected_frame_left != []:
                box_enter = False
            if object_detected == True and (res_left_hand == 1):
                box_enter = True
            if box_enter == True and res_left_hand == -1 and detected_frame_left == []:
                print("Bill entered")
                break
            
            if detected_frame_right == []:
                object_detected_right = False
            if object_detected_right == False and (detected_frame_right != []):
                object_detected_right = True
                detected_object = detected_frame_right[0]
                print(detected_object)
                # break
            if object_detected_right == True and (res_right_hand == -1) and detected_frame_right != []:
                box_enter_right = False
            if object_detected_right == True and (res_right_hand == 1):
                box_enter_right = True
            if box_enter_right == True and res_right_hand == -1 and detected_frame_right == []:
                print("Bill entered")
                break
                object_detected = False
                box_enter = False
        except(ZeroDivisionError):
            print(ZeroDivisionError)
        # frame_rightHand, frame_leftHand, right_wrist_point, left_wrist_point = wristDetectionNoCord(frame)
        if res_right_hand == 1 and res_left_hand == 1:
            coverShelfRegion(frame=frame,pts=pts1, color=(255, 255, 255))
        elif res_right_hand == 1:
            coverShelfRegion(frame=frame,pts=pts1, color= (255, 0, 255))
        elif res_left_hand == 1:
            coverShelfRegion(frame=frame,pts=pts1, color= (255, 255, 0))
        else:
            coverShelfRegion(frame=frame,pts=pts1)

        coverShelfRegion(frame=frame, pts=pts2, color= (255, 255, 0))




        cv2.imshow("YOLOv8 Inference", frame) 

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break


cap.release()
cv2.destroyAllWindows()