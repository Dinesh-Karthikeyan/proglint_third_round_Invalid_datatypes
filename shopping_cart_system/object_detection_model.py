from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def productDetection(frame):

    results = model.predict(source=frame,classes=[64,67, 73], boxes=True, save_conf=True)
    result = results[0].boxes.cls.tolist()


    y = filter(lambda x: int(x) == 39 or int(x) == 64 or int(x) == 67, result)
    # list(filter)
    # print(list(y))
    # annotated_frame = results[0].plot(line_width=1)
    return list(y)

# return annotated_frame
