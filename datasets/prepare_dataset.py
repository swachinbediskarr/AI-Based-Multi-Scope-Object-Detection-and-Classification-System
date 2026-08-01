import os
import shutil
from pathlib import Path

CURRENT_FILE = os.path.abspath(
    __file__
)

DATASETS_DIR = os.path.dirname(
    CURRENT_FILE
)

PROJECT_ROOT = os.path.dirname(
    DATASETS_DIR
)

THERMAL_DATASET_DIR = os.path.join(
    DATASETS_DIR,
    "thermal"
)

THERMAL_CLASSES = [
    "animal",
    "human",
    "vehicle"
]

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff"
}

def create_dataset_structure():

    print("\n" + "=" * 70)

    print(
        "THERMAL DATASET PREPARATION"
    )

    print("=" * 70)

    os.makedirs(
        THERMAL_DATASET_DIR,
        exist_ok=True
    )

    print(
        "\n[DATASET] Thermal dataset directory:"
    )

    print(
        THERMAL_DATASET_DIR
    )

    print(
        "\n[DATASET] Creating class directories..."
    )
    for class_name in THERMAL_CLASSES:

        class_directory = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )
        os.makedirs(
            class_directory,
            exist_ok=True
        )

        print(
            f"[CREATED] {class_directory}"
        )

def is_supported_image(
    filename
):
    extension = Path(
        filename
    ).suffix.lower()
    return (
        extension
        in
        SUPPORTED_EXTENSIONS
    )
def count_dataset_images():

    dataset_statistics = {}
    for class_name in THERMAL_CLASSES:

        class_directory = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )
        image_count = 0
        if os.path.isdir(
            class_directory
        ):

            for filename in os.listdir(
                class_directory
            ):
                file_path = os.path.join(
                    class_directory,
                    filename
                )

                if (
                    os.path.isfile(
                        file_path
                    )
                    and
                    is_supported_image(
                        filename
                    )
                ):

                    image_count += 1

        dataset_statistics[
            class_name
        ] = image_count

    return dataset_statistics

def find_unsupported_files():
    unsupported_files = []

    for class_name in THERMAL_CLASSES:

        class_directory = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )

        if not os.path.isdir(
            class_directory
        ):

            continue

        for filename in os.listdir(
            class_directory
        ):

            file_path = os.path.join(
                class_directory,
                filename
            )

            if not os.path.isfile(
                file_path
            ):
                continue

            if not is_supported_image(
                filename
            ):

                unsupported_files.append(
                    file_path
                )

    return unsupported_files

def rename_dataset_images():

    print(
        "\n[DATASET] Standardizing image filenames..."
    )

    for class_name in THERMAL_CLASSES:

        class_directory = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )

        if not os.path.isdir(
            class_directory
        ):
            continue
        image_files = []
        for filename in os.listdir(
            class_directory
        ):

            file_path = os.path.join(
                class_directory,
                filename
            )

            if (
                os.path.isfile(
                    file_path
                )
                and
                is_supported_image(
                    filename
                )
            ):
                image_files.append(
                    filename
                )
        image_files.sort()
        temporary_files = []

        for index, filename in enumerate(
            image_files,
            start=1
        ):

            old_path = os.path.join(
                class_directory,
                filename
            )

            extension = Path(
                filename
            ).suffix.lower()

            temporary_name = (
                f"temporary_"
                f"{class_name}_"
                f"{index:04d}"
                f"{extension}"
            )
            temporary_path = os.path.join(
                class_directory,
                temporary_name
            )
            os.rename(
                old_path,
                temporary_path
            )
            temporary_files.append(
                temporary_name
            )

        for index, filename in enumerate(
            temporary_files,
            start=1
        ):

            old_path = os.path.join(
                class_directory,
                filename
            )

            extension = Path(
                filename
            ).suffix.lower()

            new_name = (
                f"{class_name}_"
                f"{index:04d}"
                f"{extension}"
            )
            new_path = os.path.join(
                class_directory,
                new_name
            )
            os.rename(
                old_path,
                new_path
            )

        print(
            f"[DATASET] {class_name}: "

            f"{len(image_files)} images standardized."
        )
def print_dataset_statistics():
    statistics = (
        count_dataset_images()
    )
    print("\n" + "-" * 70)
    print(
        "THERMAL DATASET STATISTICS"
    )
    print("-" * 70)
    total_images = 0
    for class_name, image_count in (
        statistics.items()
    ):
        print(
            f"{class_name.upper():10s}"
            f": "
            f"{image_count} images"
        )
        total_images += (
            image_count
        )

    print("-" * 70)
    print(
        "TOTAL"
        f"     : "
        f"{total_images} images"
    )
    print("-" * 70)
    return statistics
def validate_dataset():

    print(
        "\n[DATASET] Validating dataset..."
    )

    statistics = (
        count_dataset_images()
    )
    dataset_ready = True

    for class_name in THERMAL_CLASSES:
        image_count = (
            statistics.get(
                class_name,
                0
            )
        )

        if image_count == 0:
            print(
                f"[WARNING] "
                f"No images found in class: "
                f"{class_name}"
            )

            dataset_ready = False

        elif image_count < 10:
            print(
                f"[WARNING] "
                f"{class_name} contains only "
                f"{image_count} images."
            )
            dataset_ready = False
        else:
            print(
                f"[OK] "
                f"{class_name}: "
                f"{image_count} images"
            )
    return dataset_ready

def create_dataset_readme():

    readme_path = os.path.join(
        DATASETS_DIR,
        "README.txt"
    )

    readme_content = """
AI-BASED MULTI-SCOPE OBJECT DETECTION AND CLASSIFICATION SYSTEM
THERMAL DATASET

============================================================
DATASET PURPOSE
============================================================

This dataset is used to train the Thermal CNN classification
module of the AI-Based Multi-Scope Object Detection and
Classification System.

============================================================
DATASET CLASSES
============================================================
1. animal
2. human
3. vehicle
============================================================
DIRECTORY STRUCTURE
============================================================
datasets/
    thermal/
        animal/
        human/
        vehicle/
============================================================
SUPPORTED IMAGE FORMATS
============================================================
.jpg
.jpeg
.png
.bmp
.tif
.tiff
============================================================
IMPORTANT
============================================================
Only actual thermal or infrared images should be used for
final CNN training and project evaluation.
The classes should remain reasonably balanced.
The training script automatically creates a training and
validation split from these class directories.
Do not place unrelated files inside the class folders.
============================================================
MODEL OUTPUT
============================================================
After successful CNN training:
models/thermal_cnn.keras
and
models/thermal_classes.json
will be generated.
============================================================
"""
    with open(
        readme_path,
        "w",
        encoding="utf-8"

    ) as file:
        file.write(
            readme_content.strip()
        )

    print(
        "\n[DATASET] README created:"
    )
    print(
        readme_path
    )

def main():
    create_dataset_structure()
    create_dataset_readme()
    unsupported_files = (
        find_unsupported_files()
    )
    if unsupported_files:
        print(
            "\n[WARNING] Unsupported files found:"
        )

        for file_path in unsupported_files:

            print(
                " -",
                file_path
            )
    print_dataset_statistics()

    dataset_ready = (
        validate_dataset()
    )
    print("\n" + "=" * 70)

    if dataset_ready:

        print(
            "THERMAL DATASET STRUCTURE IS READY"
        )
        print(
            "Dataset contains images in all required classes."
        )
    else:
        print(
            "THERMAL DATASET STRUCTURE CREATED"
        )
        print(
            "Add thermal images to the required class folders."
        )
    print("=" * 70)

    print(
        "\nDataset Location:"
    )
    print(
        THERMAL_DATASET_DIR
    )
if __name__ == "__main__":
    main()