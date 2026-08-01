import os
import cv2
from config import RGB_CAMERA_ID
from detection.yolo_detector import YOLODetector
from detection.thermal_classifier import ThermalClassifier
from detection.fusion_engine import FusionEngine

THERMAL_IMAGE_PATH = os.path.join(
    "test_images",
    "thermal_test.jpg"
)

def main():
    print("=" * 70)
    print("LIVE RGB + THERMAL CNN + FUSION TEST")
    print("=" * 70)
    print("\n[1] Loading YOLO Detector...")
    yolo_detector = YOLODetector()
    print("\n[2] Loading Thermal CNN...")
    thermal_classifier = ThermalClassifier()
    print("\n[3] Initializing Fusion Engine...")
    fusion_engine = FusionEngine(
        rgb_weight=0.60,
        thermal_weight=0.40
    )

    if not os.path.exists(
        THERMAL_IMAGE_PATH
    ):
        print(
            "[ERROR] Thermal image not found:"
        )
        print(
            THERMAL_IMAGE_PATH
        )
        return

    thermal_image = cv2.imread(
        THERMAL_IMAGE_PATH
    )

    if thermal_image is None:
        print(
            "[ERROR] Thermal image could not be read."
        )
        return

    thermal_result = (
        thermal_classifier.classify(
            thermal_image
        )
    )

    print("\nTHERMAL CNN RESULT")

    print(
        "Class:",
        thermal_result["class"]
    )

    print(
        "Confidence:",
        f"{thermal_result['confidence'] * 100:.2f}%"
    )

    camera = cv2.VideoCapture(
        RGB_CAMERA_ID
    )
    if not camera.isOpened():
        print(
            "[ERROR] RGB camera could not be opened."
        )
        return
    print(
        "\n[SYSTEM] Live Fusion System Started."
    )

    print(
        "[SYSTEM] Press Q to close."
    )

    while True:
        success, frame = camera.read()
        if not success:
            print(
                "[ERROR] Failed to read RGB frame."
            )
            break

        detections = (
            yolo_detector.detect_and_track(
                frame
            )
        )

        for detection in detections:

            x1, y1, x2, y2 = (
                detection["bbox"]
            )

            fusion_result = (
                fusion_engine.fuse(
                    rgb_result=detection,
                    thermal_result=thermal_result
                )
            )

            if (
                fusion_result["status"]
                ==
                "CONFIRMED"
            ):

                box_color = (
                    0,
                    255,
                    0
                )
            elif (
                fusion_result["status"]
                ==
                "CONFLICT"
            ):
                box_color = (
                    0,
                    165,
                    255
                )
            else:
                box_color = (
                    255,
                    255,
                    0
                )
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                2
            )
            rgb_text = (
                f"RGB: "
                f"{detection['label']} "
                f"{detection['confidence'] * 100:.1f}%"
            )
            cv2.putText(
                frame,
                rgb_text,
                (
                    x1,
                    max(
                        25,
                        y1 - 55
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                box_color,
                2
            )
            thermal_text = (
                f"THERMAL: "
                f"{thermal_result['class']} "
                f"{thermal_result['confidence'] * 100:.1f}%"
            )
            cv2.putText(
                frame,
                thermal_text,
                (
                    x1,
                    max(
                        45,
                        y1 - 30
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                box_color,
                2
            )
            fusion_text = (
                f"FUSION: "
                f"{fusion_result['final_class']} "
                f"{fusion_result['confidence'] * 100:.1f}% "
                f"[{fusion_result['status']}]"
            )
            cv2.putText(
                frame,
                fusion_text,
                (
                    x1,
                    max(
                        65,
                        y1 - 5
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                box_color,
                2
            )

        cv2.putText(
            frame,
            "RGB: YOLOv8 | THERMAL: CNN | FUSION: ACTIVE",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )
        cv2.imshow(
            "AI Multi-Scope Live Fusion",
            frame
        )

        thermal_display = (
            thermal_image.copy()
        )
        thermal_text = (
            f"CNN: "
            f"{thermal_result['class'].upper()} | "
            f"{thermal_result['confidence'] * 100:.2f}%"
        )
        cv2.putText(
            thermal_display,
            thermal_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.imshow(
            "Thermal CNN Input",
            thermal_display
        )
        if (
            cv2.waitKey(1)
            &
            0xFF
            ==
            ord("q")
        ):
            break
    camera.release()
    cv2.destroyAllWindows()
    print(
        "\n[SYSTEM] Live Fusion System Closed."
    )

if __name__ == "__main__":
    main()