"""
============================================================
DETECTION PIPELINE
AI-Based Multi-Scope Object Detection and Classification
============================================================
"""
class DetectionPipeline:
    def __init__(
        self,
        detector,
        analytics,
        fusion,
        threat,
        database,
        evidence,
        alerts
    ):

        self.detector = detector
        self.analytics = analytics
        self.fusion = fusion
        self.threat = threat
        self.database = database
        self.evidence = evidence
        self.alerts = alerts

        print("[PIPELINE] Detection Pipeline Ready")

    def process(
        self,
        frame,
        line_y,
        thermal_result,
        estimate_distance,
        get_direction
    ):

        detections = self.detector.detect_and_track(frame)
        results = []
        if detections is None:
            return results
        frame_height, frame_width = frame.shape[:2]
        for detection in detections:
            label = detection["label"]
            confidence = float(
                detection["confidence"]
            )

            bbox = detection["bbox"]
            x1, y1, x2, y2 = bbox
            width = detection["width"]
            center_x = detection["center"][0]
            distance = estimate_distance(
                width
            )
            direction = get_direction(
                center_x,
                frame_width
            )
            analytics_events = (
                self.analytics.process_detection(
                    detection,
                    line_y
                )
            )

            fusion_result = (
                self.fusion.fuse(
                    rgb_result=detection,
                    thermal_result=thermal_result
                )
            )
            threat = (
                self.threat.analyze(
                    label,
                    distance,
                    confidence
                )
            )

            results.append({
                "detection": detection,
                "distance": distance,
                "direction": direction,
                "fusion": fusion_result,
                "threat": threat,
                "events": analytics_events
            })
        return results