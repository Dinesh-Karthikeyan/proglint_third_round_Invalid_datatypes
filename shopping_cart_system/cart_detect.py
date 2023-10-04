from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def cartDetection(frame):
    results = model.predict(source=frame, classes=[26], boxes=True, save_conf=True)
    result = results[0].boxes.xyxy
    annotated_frame = results[0].plot(line_width=3)

    return annotated_frame
