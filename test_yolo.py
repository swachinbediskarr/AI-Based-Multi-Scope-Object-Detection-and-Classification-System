import cv2
from ultralytics import YOLO
model = YOLO("models/yolov8s.pt")
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    results = model(frame)
    annotated = results[0].plot()
    cv2.imshow("YOLO", annotated)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()