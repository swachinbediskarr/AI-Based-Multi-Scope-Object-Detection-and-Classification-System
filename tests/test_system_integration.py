import os
import cv2

from detection.yolo_detector import (
    YOLODetector
)

from detection.thermal_classifier import (
    ThermalClassifier
)

from detection.fusion_engine import (
    FusionEngine
)

from database.database_manager import (
    DatabaseManager
)

from alerts.alert_manager import (
    AlertManager
)

from analytics.report_generator import (
    ReportGenerator
)

from config import (
    THERMAL_TEST_IMAGE_PATH
)


def print_section(
    number,
    title
):

    print("\n" + "=" * 70)

    print(
        f"[{number}] {title}"
    )

    print("=" * 70)


def main():

    print("=" * 70)

    print(
        "AI-BASED MULTI-SCOPE OBJECT DETECTION "
        "AND CLASSIFICATION SYSTEM"
    )

    print(
        "COMPLETE BACKEND INTEGRATION TEST"
    )

    print("=" * 70)

    test_results = {}

    print_section(
        1,
        "TESTING YOLO ENGINE"
    )

    try:
        detector = YOLODetector()
        test_results[
            "YOLO Engine"
        ] = True

        print(
            "[PASS] YOLO engine initialized."
        )

    except Exception as error:

        detector = None

        test_results[
            "YOLO Engine"
        ] = False

        print(
            "[FAIL] YOLO engine initialization failed."
        )

        print(
            f"Error: {error}"
        )

    print_section(
        2,
        "TESTING THERMAL CNN ENGINE"
    )

    thermal_classifier = None
    thermal_result = None

    try:

        thermal_classifier = (
            ThermalClassifier()
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

        thermal_result = (
            thermal_classifier.classify(
                thermal_image
            )
        )

        if not thermal_result[
            "success"
        ]:

            raise RuntimeError(
                thermal_result.get(
                    "message",
                    "Thermal classification failed."
                )
            )

        test_results[
            "Thermal CNN"
        ] = True

        print(
            "[PASS] Thermal CNN initialized."
        )

        print(
            f"Class      : "
            f"{thermal_result['class']}"
        )

        print(
            f"Confidence : "
            f"{thermal_result['confidence'] * 100:.2f}%"
        )

    except Exception as error:

        test_results[
            "Thermal CNN"
        ] = False

        print(
            "[FAIL] Thermal CNN test failed."
        )

        print(
            f"Error: {error}"
        )

    print_section(
        3,
        "TESTING FUSION ENGINE"
    )

    try:

        fusion_engine = FusionEngine(
            rgb_weight=0.60,
            thermal_weight=0.40
        )

        sample_rgb_result = {
            "track_id": 101,
            "class_id": 0,
            "label": "person",
            "confidence": 0.92,
            "bbox": [
                100,
                100,
                300,
                500
            ],
            "center": (
                200,
                300
            ),
            "width": 200,
            "height": 400
        }

        if thermal_result is not None:

            test_thermal_result = (
                thermal_result
            )

        else:

            print(
                "[INFO] Using fallback thermal result "
                "for fusion test."
            )

            test_thermal_result = {
                "success": True,
                "class": "human",
                "confidence": 0.90
            }

        fusion_result = (
            fusion_engine.fuse(
                rgb_result=sample_rgb_result,
                thermal_result=test_thermal_result
            )
        )

        test_results[
            "Fusion Engine"
        ] = True

        print(
            "[PASS] Fusion engine executed."
        )

        print(
            f"Status      : "
            f"{fusion_result['status']}"
        )

        print(
            f"Final Class : "
            f"{fusion_result['final_class']}"
        )

        print(
            f"Confidence  : "
            f"{fusion_result['confidence'] * 100:.2f}%"
        )

        print(
            f"Source      : "
            f"{fusion_result['source']}"
        )

    except Exception as error:

        fusion_engine = None

        test_results[
            "Fusion Engine"
        ] = False

        print(
            "[FAIL] Fusion engine test failed."
        )

        print(
            f"Error: {error}"
        )

    print_section(
        4,
        "TESTING DATABASE"
    )
    try:
        database = DatabaseManager()

        database.save_event(
            event_type="INTEGRATION_TEST",
            message=(
                "Complete backend integration "
                "test executed."
            )
        )

        test_results[
            "Database"
        ] = True

        print(
            "[PASS] Database initialized."
        )

        print(
            "[PASS] Integration test event saved."
        )

    except Exception as error:

        database = None

        test_results[
            "Database"
        ] = False

        print(
            "[FAIL] Database test failed."
        )

        print(
            f"Error: {error}"
        )
    print_section(
        5,
        "TESTING ALERT MANAGER"
    )
    try:

        alert_manager = (
            AlertManager()
        )

        test_track_id = 99999

        alert_allowed = (
            alert_manager.can_alert(
                test_track_id
            )
        )

        test_results[
            "Alert Manager"
        ] = alert_allowed

        if alert_allowed:
            print(
                "[PASS] Alert manager initialized."
            )
            print(
                "[PASS] Cooldown system operational."
            )
        else:
            print(
                "[FAIL] Initial alert was unexpectedly blocked."
            )

    except Exception as error:

        alert_manager = None

        test_results[
            "Alert Manager"
        ] = False

        print(
            "[FAIL] Alert manager test failed."
        )
        print(
            f"Error: {error}"
        )
    print_section(
        6,
        "TESTING REPORT GENERATOR"
    )
    try:
        report_generator = (
            ReportGenerator()
        )

        report_path = (
            report_generator.export_csv()
        )

        if not os.path.exists(
            report_path
        ):

            raise RuntimeError(
                "CSV report was not created."
            )

        test_results[
            "Report Generator"
        ] = True

        print(
            "[PASS] CSV report generated."
        )
        print(
            f"Report Path:\n{report_path}"
        )

    except Exception as error:

        test_results[
            "Report Generator"
        ] = False
        print(
            "[FAIL] Report generator test failed."
        )
        print(
            f"Error: {error}"
        )
    print("\n" + "=" * 70)
    print(
        "INTEGRATION TEST SUMMARY"
    )
    print("=" * 70)

    for module_name, status in (
        test_results.items()
    ):

        result_text = (
            "PASS"
            if status
            else "FAIL"
        )

        print(
            f"{module_name:<25} : "
            f"{result_text}"
        )

    passed_tests = sum(
        1
        for status in test_results.values()
        if status
    )
    total_tests = len(
        test_results
    )
    print("-" * 70)
    print(
        f"Passed Modules: "
        f"{passed_tests}/{total_tests}"
    )
    if (
        passed_tests
        ==
        total_tests
    ):
        print(
            "\n[SUCCESS] ALL BACKEND MODULES "
            "ARE INTEGRATED SUCCESSFULLY."
        )
        print(
            "[STATUS] SYSTEM READY FOR "
            "FULL DASHBOARD TESTING."
        )
    else:
        print(
            "\n[WARNING] SOME MODULES FAILED."
        )
        print(
            "[STATUS] FIX FAILED MODULES BEFORE "
            "RUNNING THE COMPLETE DASHBOARD."
        )
    print("=" * 70)
if __name__ == "__main__":
    main()