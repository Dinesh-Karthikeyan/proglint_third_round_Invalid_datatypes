from ultralytics import YOLO

model = YOLO("yolov8n-pose.pt")

height = 200
width = 200

def wristDetection(frame):
 
    body_points = model(frame)
    right_wrist_point = []
    left_wrist_point = []

    for points in body_points:
        xy_points = points.keypoints.xy
        
        try:
            right_wrist_point_tensor = xy_points[0][10]
            left_wrist_point_tensor = xy_points[0][9]
        except IndexError:
            print(IndexError)
        
        
    x_right_wrist_point = int(right_wrist_point_tensor[0].tolist())
    y_right_wrist_point = int(right_wrist_point_tensor[1].tolist())
    right_wrist_point.append(x_right_wrist_point)
    right_wrist_point.append(y_right_wrist_point)
    
    x_left_wrist_point = int(left_wrist_point_tensor[0].tolist())
    y_left_wrist_point = int(left_wrist_point_tensor[1].tolist())
    left_wrist_point.append(x_left_wrist_point)
    left_wrist_point.append(y_left_wrist_point)

    top_left_cord_x_rightHand = x_right_wrist_point - width // 2
    top_left_cord_y_rightHand =  y_right_wrist_point - height 
    bottom_right_cord_x_rightHand = x_right_wrist_point + width // 2
    bottom_right_cord_y_rightHand = y_right_wrist_point 

    try:
        frame_rightHand = frame[top_left_cord_y_rightHand:bottom_right_cord_y_rightHand, top_left_cord_x_rightHand:bottom_right_cord_y_rightHand]
        top_left_cord_rightHand = (top_left_cord_x_rightHand , top_left_cord_y_rightHand )
        bottom_right_cord_rightHand = (bottom_right_cord_x_rightHand, bottom_right_cord_y_rightHand )
    except(ValueError):
        print(ValueError)
    

    top_left_cord_x_leftHand = x_left_wrist_point - width // 2
    top_left_cord_y_leftHand = y_left_wrist_point - height
    bottom_right_cord_x_leftHand = x_left_wrist_point + width // 2
    bottom_right_cord_y_leftHand = y_left_wrist_point 

    

    try:
        frame_leftHand = frame[top_left_cord_y_leftHand:bottom_right_cord_y_leftHand, top_left_cord_x_leftHand:bottom_right_cord_y_leftHand]
        top_left_cord_leftHand = (top_left_cord_x_leftHand, top_left_cord_y_leftHand)
        bottom_right_cord_leftHand  = (bottom_right_cord_x_leftHand, bottom_right_cord_y_leftHand)
    except(ValueError):
        print(ValueError)

    return top_left_cord_rightHand, bottom_right_cord_rightHand, top_left_cord_leftHand, bottom_right_cord_leftHand, frame_rightHand, frame_leftHand, right_wrist_point, left_wrist_point

# ------------------------------------------------------
def wristDetectionNoCord(frame):
 
    body_points = model(frame)
    right_wrist_point = []
    left_wrist_point = []

    for points in body_points:
        xy_points = points.keypoints.xy
        
        try:
            right_wrist_point_tensor = xy_points[0][10]
            left_wrist_point_tensor = xy_points[0][9]
        except IndexError:
            print(IndexError)
        
        
    x_right_wrist_point = int(right_wrist_point_tensor[0].tolist())
    y_right_wrist_point = int(right_wrist_point_tensor[1].tolist())
    right_wrist_point.append(x_right_wrist_point)
    right_wrist_point.append(y_right_wrist_point)
    
    x_left_wrist_point = int(left_wrist_point_tensor[0].tolist())
    y_left_wrist_point = int(left_wrist_point_tensor[1].tolist())
    left_wrist_point.append(x_left_wrist_point)
    left_wrist_point.append(y_left_wrist_point)

    top_left_cord_x_rightHand = right_wrist_point[0] - width // 2
    top_left_cord_y_rightHand =  left_wrist_point[1] - height
    bottom_right_cord_x_rightHand = left_wrist_point[0] + width // 2
    bottom_right_cord_y_rightHand = left_wrist_point[1] 

    try:
        frame_rightHand = frame[top_left_cord_y_rightHand:bottom_right_cord_y_rightHand, top_left_cord_x_rightHand:bottom_right_cord_y_rightHand]
        top_left_cord_rightHand = (top_left_cord_x_rightHand , top_left_cord_y_rightHand )
        bottom_right_cord_rightHand = (bottom_right_cord_x_rightHand, bottom_right_cord_y_rightHand )
    except(ValueError):
        print(ValueError)
    

    top_left_cord_x_leftHand = x_left_wrist_point - width // 2
    top_left_cord_y_leftHand = y_left_wrist_point - height
    bottom_right_cord_x_leftHand = x_left_wrist_point + width // 2
    bottom_right_cord_y_leftHand = y_left_wrist_point

    

    try:
        frame_leftHand = frame[top_left_cord_y_leftHand:bottom_right_cord_y_leftHand, top_left_cord_x_leftHand:bottom_right_cord_y_leftHand]
        top_left_cord_leftHand = (top_left_cord_x_leftHand, top_left_cord_y_leftHand)
        bottom_right_cord_leftHand  = (bottom_right_cord_x_leftHand, bottom_right_cord_y_leftHand)
    except(ValueError):
        print(ValueError)

    return frame_rightHand, frame_leftHand, right_wrist_point, left_wrist_point