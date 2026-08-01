import time
from collections import deque

class AnalyticsManager:
    """
    Advanced Analytics Manager
    - Unique Person Count
    - Unique Vehicle Count
    - Unique Animal Count
    - Entry / Exit Counter
    - Total Detections
    - Average Confidence
    - Highest Confidence
    - Detection History
    - Session Runtime
    """

    def __init__(self):

        self.start_time = time.time()

        self.person_ids = set()
        self.vehicle_ids = set()
        self.animal_ids = set()

        self.tracked_positions = {}

        self.entry_count = 0
        self.exit_count = 0

        self.total_detections = 0

        self.total_confidence = 0.0
        self.highest_confidence = 0.0

        self.history = deque(maxlen=500)

        self.vehicle_classes = {
            "car",
            "motorcycle",
            "bus",
            "truck"
        }

        self.animal_classes = {
            "dog",
            "cat",
            "horse",
            "cow",
            "sheep",
            "bird"
        }

        print("[ANALYTICS] Advanced Analytics Initialized")

    def process_detection(
        self,
        detection,
        line_y
    ):

        events = []

        track_id = detection["track_id"]
        label = detection["label"]
        confidence = float(detection["confidence"])
        center_y = detection["center"][1]

        self.total_detections += 1

        self.total_confidence += confidence

        self.highest_confidence = max(
            self.highest_confidence,
            confidence
        )

        if label == "person":
            self.person_ids.add(track_id)

        elif label in self.vehicle_classes:
            self.vehicle_ids.add(track_id)

        elif label in self.animal_classes:
            self.animal_ids.add(track_id)

        self.history.append({
            "track_id": track_id,
            "label": label,
            "confidence": confidence,
            "time": time.strftime("%H:%M:%S")
        })

        if track_id in self.tracked_positions:
            previous = self.tracked_positions[track_id]
            if previous <= line_y < center_y:
                self.entry_count += 1

                events.append({
                    "type": "ENTRY",
                    "track_id": track_id,
                    "label": label,
                    "message":
                        f"{label.upper()} #{track_id} ENTERED"
                })
            elif previous >= line_y > center_y:
                self.exit_count += 1
                events.append({
                    "type": "EXIT",
                    "track_id": track_id,
                    "label": label,
                    "message":
                        f"{label.upper()} #{track_id} EXITED"
                })
        self.tracked_positions[track_id] = center_y
        return events

    def get_statistics(self):

        runtime = int(time.time() - self.start_time)

        if self.total_detections == 0:
            average = 0.0
        else:
            average = (
                self.total_confidence /
                self.total_detections
            )

        return {
            "unique_persons":
                len(self.person_ids),

            "unique_vehicles":
                len(self.vehicle_ids),

            "unique_animals":
                len(self.animal_ids),

            "entries":
                self.entry_count,

            "exits":
                self.exit_count,

            "total_detections":
                self.total_detections,

            "average_confidence":
                round(average * 100, 2),

            "highest_confidence":
                round(
                    self.highest_confidence * 100,
                    2
                ),
            "runtime":
                runtime
        }
    def get_recent_history(
        self,
        limit=10
    ):
        return list(self.history)[-limit:]
    def reset_statistics(self):
        self.__init__()