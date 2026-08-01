import csv
import os
from analytics.report_generator import (
    ReportGenerator
)
def main():
    print("=" * 60)
    print(
        "REPORT GENERATOR TEST"
    )
    print("=" * 60)
    print(
        "\n[TEST] Initializing Report Generator..."
    )
    report_generator = (
        ReportGenerator()
    )

    print(
        "[TEST] Report Generator initialized successfully."
    )

    print(
        "\n[TEST] Generating CSV report..."
    )
    try:
        file_path = (
            report_generator.export_csv()
        )
    except Exception as error:

        print(
            "\n[FAIL] CSV report generation failed."
        )
        print(
            f"Error: {error}"
        )
        return
    print(
        f"\nGenerated File:\n{file_path}"
    )

    if not os.path.exists(
        file_path
    ):
        print(
            "\n[FAIL] CSV file was not created."
        )
        return
    print(
        "\n[PASS] CSV file created successfully."
    )
    file_size = os.path.getsize(
        file_path
    )

    print(
        f"[INFO] File Size: "
        f"{file_size} bytes"
    )

    if file_size == 0:
        print(
            "[FAIL] CSV file is empty."
        )
        return
    print(
        "[PASS] CSV file contains data."
    )
    print(
        "\n[TEST] Reading generated CSV file..."
    )

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        reader = csv.reader(
            csv_file
        )

        rows = list(
            reader
        )

    expected_header = [
        "ID",
        "Timestamp",
        "Track ID",
        "Label",
        "Confidence",
        "Estimated Distance",
        "Direction",
        "Alert Status",
        "Snapshot Path"
    ]

    if not rows:
        print(
            "[FAIL] No rows found in CSV file."
        )
        return
    actual_header = rows[0]
    if (
        actual_header
        ==
        expected_header
    ):
        print(
            "[PASS] CSV header is correct."
        )
    else:

        print(
            "[FAIL] CSV header does not match."
        )

        print(
            f"Expected: {expected_header}"
        )
        print(
            f"Actual  : {actual_header}"
        )
    data_rows = rows[1:]
    print(
        f"\n[INFO] Exported Detection Records: "
        f"{len(data_rows)}"
    )
    if data_rows:
        print(
            "\nSample Exported Records:"
        )
        print("-" * 60)
        for row in data_rows[:5]:

            print(
                row
            )
    else:
        print(
            "\n[INFO] Database currently contains "
            "no detection records."
        )
        print(
            "[INFO] CSV structure is still valid."
        )
    print("\n" + "=" * 60)
    print(
        "[TEST] REPORT GENERATOR TEST COMPLETED"
    )
    print("=" * 60)
if __name__ == "__main__":
    main()