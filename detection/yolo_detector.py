from ultralytics import YOLO
from config import (
    YOLO_MODEL_PATH,
    YOLO_CONFIDENCE,
    YOLO_IMAGE_SIZE
)

class YOLODetector:
    """
    RGB Object Detection, Multi-Object Tracking & Distance Estimation
    """
    def __init__(self):

        print("[AI] Loading YOLO model...")
        self.model = YOLO(YOLO_MODEL_PATH)
        print("[AI] YOLO model loaded successfully.")

    def estimate_distance(self, bbox_height, frame_height):
        """
        Calculates approximate distance (in meters) based on bounding box height relative to frame height.
        """
        if bbox_height <= 0:
            return 5.0

        focal_factor = frame_height * 0.8
        distance = focal_factor / bbox_height
        return round(max(0.3, min(distance, 10.0)), 2)

    def detect_and_track(self, frame):
        detections = []
        if frame is None:
            return detections

        try:
            frame_height, frame_width = frame.shape[:2]
            results = self.model.track(
                source=frame,
                persist=True,
                conf=YOLO_CONFIDENCE,
                imgsz=YOLO_IMAGE_SIZE,
                verbose=False
            )
            if not results:
                return detections
            for result in results:
                if result.boxes is None:
                    continue
                boxes = result.boxes
                ids = boxes.id
                if ids is None:
                    ids = [-1] * len(boxes)
                else:
                    ids = ids.int().cpu().tolist()
                class_ids = boxes.cls.int().cpu().tolist()
                confidences = boxes.conf.cpu().tolist()
                bounding_boxes = (
                    boxes.xyxy
                    .int()
                    .cpu()
                    .tolist()
                )

                for i in range(len(bounding_boxes)):
                    x1, y1, x2, y2 = bounding_boxes[i]

                    width = max(1, x2 - x1)
                    height = max(1, y2 - y1)

                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    class_id = class_ids[i]
                    label = self.model.names[class_id]
                    confidence = float(confidences[i])

                    distance = self.estimate_distance(height, frame_height)

                    if distance < 1.5:
                        status = "CRITICAL"
                    elif distance < 3.0:
                        status = "WARNING"
                    else:
                        status = "SAFE"
                    detection = {
                        "track_id": ids[i],
                        "class_id": class_id,
                        "label": label,
                        "confidence": confidence,

                        "bbox": (
                            x1,
                            y1,
                            x2,
                            y2
                        ),

                        "center": (
                            center_x,
                            center_y
                        ),

                        "width": width,
                        "height": height,
                        "distance": distance,  
                        "status": status
                    }
                    detections.append(detection)
            return detections
        except Exception as error:
            print("[YOLO ERROR]", error)
            return []