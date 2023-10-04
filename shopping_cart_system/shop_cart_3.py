import cv2
from object_detection_model import productDetection
from wrist_detection_model import wristDetection, wristDetectionNoCord
from shelf_region import coverShelfRegion
from cart_detect import cartDetection
import numpy as np
import requests
url = "https://shopping-cart-server-production.up.railway.app/customer_cart"

cap = cv2.VideoCapture(0)

pts1 = np.array([[50,10],[200,50],[200,200],[50,200]], np.int32)
pts1 = pts1.reshape((-1,1,2))
product = {"cartid": 421, "bottle": 0, "cellphone": 0, "mouse": 0, "totalcost": 0, "paid":False}
pts2 = np.array([[200,300],[400,300],[400,400],[200,450]], np.int32)
pts2 = pts2.reshape((-1,1,2))
detected_frame_right = [0]
flag_tc_shelf = False
flag_tc_cart = False

flag_ts_shelf = False
flag_ts_cart = False

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
            flag_tc_shelf = True

        res_right_hand_cart = insideBox(pts2, right_wrist_point)
        if res_right_hand_cart == 1:
            print("cart")
            flag_ts_shelf = True

        try:
            if flag_tc_shelf:
                detected_frame_right = productDetection(frame=frame_rightHand)
                if len(detected_frame_right) > 0:
                    print("predicted------------------------------------------------------>>>")
                    flag_tc_shelf = False
                    flag_tc_cart = True

            if flag_ts_shelf:
                detected_frame_right_s = productDetection(frame=frame_rightHand)
                if len(detected_frame_right_s) > 0:
                    # product["p2"] = "0"
                    flag_ts_cart = False

        except(ZeroDivisionError):
            print(ZeroDivisionError)
        

        if flag_tc_cart:
            res_right_hand_cart_c = insideBox(pts2, right_wrist_point)
            if res_right_hand_cart_c == 1 and len(detected_frame_right) > 0:
                if detected_frame_right[0] == 39:
                    product["bottle"] += 1

                if detected_frame_right[0] == 73:
                    product["book"] += 1

                if detected_frame_right[0] == 67:
                    product["cellphone"] += 1
            
                flag_tc_cart = False
        

        if flag_ts_shelf:
            res_right_hand_shelf_d = insideBox(pts1, right_wrist_point)
            if res_right_hand_shelf_d == 1 and len(detected_frame_right_s) > 0:
                if detected_frame_right_s[0] == 39:
                    product["bottle"] -= 1

                if detected_frame_right_s[0] == 73:
                    product["book"] -= 1

                if detected_frame_right_s[0] == 67:
                    product["cellphone"] -= 1

                flag_ts_cart = True


        print(product)
        coverShelfRegion(frame=frame,pts=pts1)

        coverShelfRegion(frame=frame, pts=pts2, color= (255, 255, 0))

        cv2.imshow("YOLOv8 Inference", frame) 

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break



data = product

response = requests.post(url, json=data)

if response.status_code == 200:
    print("POST request successful")
else:
    print(response.status_code, response.content)

cap.release()
cv2.destroyAllWindows()