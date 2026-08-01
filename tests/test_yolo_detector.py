import cv2
from detection.yolo_detector import YOLODetector
from config import (
    RGB_CAMERA_ID,
    CAMERA_WIDTH,
    CAMERA_HEIGHT
)
def main():

    print("=" * 60)
    print("YOLO DETECTOR TEST")
    print("=" * 60)
    print("\n[TEST] Loading YOLO detector...")
    detector = YOLODetector()
    print("\n[TEST] Opening RGB camera...")

    camera = cv2.VideoCapture(
        RGB_CAMERA_ID
    )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT
    )

    if not camera.isOpened():

        raise RuntimeError(
            "RGB camera could not be opened."
        )

    print(
        "[TEST] Camera opened successfully."
    )

    print(
        "\nPress Q to stop the test."
    )

    while True:

        success, frame = camera.read()

        if not success:

            print(
                "[ERROR] Could not read camera frame."
            )

            break

        detections = (
            detector.detect_and_track(
                frame
            )
        )

        for detection in detections:

            track_id = detection[
                "track_id"
            ]

            label = detection[
                "label"
            ]

            confidence = detection[
                "confidence"
            ]

            x1, y1, x2, y2 = detection[
                "bbox"
            ]

            center_x, center_y = detection[
                "center"
            ]

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Center point
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

            # Detection information
            text = (
                f"{label.upper()} "
                f"ID:{track_id} "
                f"{confidence * 100:.1f}%"
            )

            cv2.putText(
                frame,
                text,
                (
                    x1,
                    max(
                        25,
                        y1 - 10
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            print(
                f"Track ID: {track_id} | "
                f"Class: {label} | "
                f"Confidence: {confidence:.4f} | "
                f"BBox: {detection['bbox']}"
            )

        cv2.putText(
            frame,
            f"Objects: {len(detections)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )
        cv2.imshow(
            "YOLO Detection and Tracking Test",
            frame
        )
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()
    print(
        "\n[TEST] YOLO detector test completed."
    )
if __name__ == "__main__":
    main()