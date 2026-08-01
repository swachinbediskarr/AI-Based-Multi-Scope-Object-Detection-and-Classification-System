import os
import cv2

from detection.thermal_classifier import (
    ThermalClassifier
)

from config import (
    THERMAL_TEST_IMAGE_PATH
)

def main():

    print("=" * 60)

    print(
        "THERMAL CNN CLASSIFIER TEST"
    )

    print("=" * 60)

    print(
        "\n[TEST] Checking thermal test image..."
    )

    if not os.path.exists(
        THERMAL_TEST_IMAGE_PATH
    ):

        raise FileNotFoundError(
            f"Thermal test image not found:\n"
            f"{THERMAL_TEST_IMAGE_PATH}"
        )

    thermal_image = cv2.imread(
        THERMAL_TEST_IMAGE_PATH
    )

    if thermal_image is None:

        raise RuntimeError(
            "Thermal test image could not be read."
        )
    print(
        "[TEST] Thermal image loaded successfully."
    )
    print(
        "\n[TEST] Loading Thermal CNN classifier..."
    )
    classifier = ThermalClassifier()
    print(
        "\n[TEST] Running thermal classification..."
    )
    result = classifier.classify(
        thermal_image
    )
    print("\n" + "=" * 60)
    print(
        "THERMAL CLASSIFICATION RESULT"
    )
    print("=" * 60)
    print(
        f"Success     : {result['success']}"
    )
    print(
        f"Class       : {result['class']}"
    )

    print(
        f"Confidence  : "
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        "\nAll Class Probabilities:"
    )

    for class_name, probability in zip(
        classifier.class_names,
        result["all_probabilities"]
    ):

        print(
            f"  {class_name:<15} : "
            f"{probability * 100:.2f}%"
        )

    display_image = (
        thermal_image.copy()
    )

    result_text = (
        f"CNN: "
        f"{result['class'].upper()} "
        f"{result['confidence'] * 100:.2f}%"
    )

    cv2.putText(
        display_image,
        result_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Thermal CNN Classification Test",
        display_image
    )

    print(
        "\nPress any key on the image window to close."
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(
        "\n[TEST] Thermal classifier test completed."
    )
if __name__ == "__main__":
    main()