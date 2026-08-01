import os
PROJECT_NAME = (
    "AI-Based Multi-Scope Object Detection "
    "and Classification System"
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

DATASETS_DIR = os.path.join(
    BASE_DIR,
    "datasets"
)

THERMAL_DATASET_DIR = os.path.join(
    DATASETS_DIR,
    "thermal"
)

TEST_IMAGES_DIR = os.path.join(
    BASE_DIR,
    "test_images"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

EVIDENCE_DIR = os.path.join(
    BASE_DIR,
    "evidence"
)

REPORTS_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

LOGS_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

REQUIRED_DIRECTORIES = [
    MODELS_DIR,
    DATASETS_DIR,
    THERMAL_DATASET_DIR,
    TEST_IMAGES_DIR,
    DATABASE_DIR,
    EVIDENCE_DIR,
    REPORTS_DIR,
    LOGS_DIR
]

for directory in REQUIRED_DIRECTORIES:

    os.makedirs(
        directory,
        exist_ok=True
    )

YOLO_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "yolov8s.pt"
)
YOLO_CONFIDENCE = 0.45
YOLO_IMAGE_SIZE = 640
RGB_CAMERA_ID = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
LINE_Y_PERCENTAGE = 0.60
PROXIMITY_THRESHOLD = 1.5
KNOWN_OBJECT_WIDTH = 0.5
FOCAL_LENGTH = 600
VOICE_ALERT_ENABLED = True
ALERT_COOLDOWN = 5
ALERT_CLASSES = {

    "person",
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck",
    "dog"
}

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "security_system.db"
)

THERMAL_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "thermal_cnn.keras"
)

THERMAL_CLASSES_PATH = os.path.join(
    MODELS_DIR,
    "thermal_classes.json"
)

THERMAL_IMAGE_WIDTH = 224
THERMAL_IMAGE_HEIGHT = 224
THERMAL_BATCH_SIZE = 32
THERMAL_EPOCHS = 30
THERMAL_CLASS_NAMES = [

    "animal",
    "human",
    "vehicle"
]

THERMAL_INPUT_MODE = "IMAGE"

PREFERRED_THERMAL_TEST_IMAGE = os.path.join(
    TEST_IMAGES_DIR,
    "thermal_test.jpg"
)

THERMAL_TEST_IMAGE_CANDIDATES = [

    os.path.join(
        TEST_IMAGES_DIR,
        "thermal_test.jpg"
    ),

    os.path.join(
        TEST_IMAGES_DIR,
        "thermal_test.jpeg"
    ),

    os.path.join(
        TEST_IMAGES_DIR,
        "thermal_test.png"
    ),

    os.path.join(
        TEST_IMAGES_DIR,
        "thermal_test.bmp"
    )
]

THERMAL_TEST_IMAGE_PATH = (
    PREFERRED_THERMAL_TEST_IMAGE
)

for image_path in THERMAL_TEST_IMAGE_CANDIDATES:

    if os.path.isfile(
        image_path
    ):

        THERMAL_TEST_IMAGE_PATH = (
            image_path
        )

        break

THERMAL_CAMERA_ID = 1
THERMAL_CLASSIFICATION_INTERVAL = 2.0
DEBUG_CONFIG = True

def validate_configuration():

    """
    Checks important project paths and files.
    Returns:
        dict:
            Configuration validation results.
    """
    results = {

        "base_directory_exists":
            os.path.isdir(
                BASE_DIR
            ),

        "models_directory_exists":
            os.path.isdir(
                MODELS_DIR
            ),

        "test_images_directory_exists":
            os.path.isdir(
                TEST_IMAGES_DIR
            ),

        "yolo_model_exists":
            os.path.isfile(
                YOLO_MODEL_PATH
            ),

        "thermal_model_exists":
            os.path.isfile(
                THERMAL_MODEL_PATH
            ),

        "thermal_classes_exists":
            os.path.isfile(
                THERMAL_CLASSES_PATH
            ),

        "thermal_test_image_exists":
            os.path.isfile(
                THERMAL_TEST_IMAGE_PATH
            )
    }

    return results

if DEBUG_CONFIG:

    print("\n" + "=" * 70)

    print(
        "PROJECT CONFIGURATION CHECK"
    )

    print("=" * 70)

    print(
        "\n[CONFIG] BASE DIRECTORY:"
    )

    print(
        BASE_DIR
    )

    print(
        "\n[CONFIG] MODELS DIRECTORY:"
    )

    print(
        MODELS_DIR
    )

    print(
        "\n[CONFIG] YOLO MODEL:"
    )

    print(
        YOLO_MODEL_PATH
    )

    print(
        "[CONFIG] YOLO MODEL EXISTS:",
        os.path.isfile(
            YOLO_MODEL_PATH
        )
    )

    print(
        "\n[CONFIG] THERMAL CNN MODEL:"
    )

    print(
        THERMAL_MODEL_PATH
    )

    print(
        "[CONFIG] THERMAL CNN MODEL EXISTS:",
        os.path.isfile(
            THERMAL_MODEL_PATH
        )
    )

    print(
        "\n[CONFIG] THERMAL CLASS FILE:"
    )

    print(
        THERMAL_CLASSES_PATH
    )

    print(
        "[CONFIG] THERMAL CLASS FILE EXISTS:",
        os.path.isfile(
            THERMAL_CLASSES_PATH
        )
    )

    print(
        "\n[CONFIG] TEST IMAGES DIRECTORY:"
    )

    print(
        TEST_IMAGES_DIR
    )

    print(
        "[CONFIG] TEST IMAGES DIRECTORY EXISTS:",
        os.path.isdir(
            TEST_IMAGES_DIR
        )
    )
    print(
        "\n[CONFIG] SELECTED THERMAL TEST IMAGE:"
    )

    print(
        THERMAL_TEST_IMAGE_PATH
    )

    print(
        "[CONFIG] THERMAL TEST IMAGE EXISTS:",
        os.path.isfile(
            THERMAL_TEST_IMAGE_PATH
        )
    )

    print(
        "\n[CONFIG] FILES INSIDE TEST_IMAGES:"
    )
    try:
        files = os.listdir(
            TEST_IMAGES_DIR
        )
        if files:
            for filename in files:
                print(
                    " -",
                    repr(
                        filename
                    )
                )
        else:
            print(
                " - No files found."
            )

    except Exception as error:

        print(
            "[CONFIG] Could not read test_images directory:"
        )
        print(
            error
        )
    print(
        "\n[CONFIG] VALIDATION SUMMARY:"
    )
    validation_results = (
        validate_configuration()
    )
    for key, value in (
        validation_results.items()
    ):

        print(
            f" - {key}: {value}"
        )


    print("\n" + "=" * 70)

    print(
        "END OF CONFIGURATION CHECK"
    )

    print("=" * 70 + "\n")