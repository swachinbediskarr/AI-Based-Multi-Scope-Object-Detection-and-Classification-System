import os
from pathlib import Path

DATASETS_DIR = os.path.dirname(
    os.path.abspath(__file__)
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

def count_images(
    directory
):
    count = 0
    if not os.path.isdir(
        directory
    ):
        return count

    for filename in os.listdir(
        directory
    ):
        file_path = os.path.join(
            directory,
            filename
        )

        extension = Path(
            filename
        ).suffix.lower()

        if (
            os.path.isfile(
                file_path
            )
            and
            extension
            in
            SUPPORTED_EXTENSIONS
        ):
            count += 1
    return count

def main():
    print("\n" + "=" * 70)
    print(
        "THERMAL DATASET INFORMATION"
    )
    print("=" * 70)
    print(
        "\nDataset Directory:"
    )
    print(
        THERMAL_DATASET_DIR
    )
    print("\n" + "-" * 70)
    print(
        "CLASS STATISTICS"
    )
    print("-" * 70)
    total_images = 0
    for class_name in THERMAL_CLASSES:
        class_directory = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )
        image_count = count_images(
            class_directory
        )
        total_images += (
            image_count
        )

        print(
            f"{class_name.upper():10s}"
            f": "
            f"{image_count} images"
        )
    print("-" * 70)
    print(
        f"TOTAL     : "
        f"{total_images} images"
    )

    print("-" * 70)
    if total_images == 0:
        print(
            "\n[STATUS] Dataset folders are ready."
        )

        print(
            "[STATUS] Thermal images still need to be added."
        )

    else:
        print(
            "\n[STATUS] Dataset contains images."
        )
        print(
            "[STATUS] Verify class balance before training."
        )

    print("\n" + "=" * 70)
if __name__ == "__main__":
    main()