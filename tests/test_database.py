from database.database_manager import (
    DatabaseManager
)
def main():
    print("=" * 60)
    print(
        "DATABASE MANAGER TEST"
    )
    print("=" * 60)
    print(
        "\n[TEST] Initializing database..."
    )
    database = DatabaseManager()
    print(
        "[TEST] Database initialized successfully."
    )
    print(
        "\n[TEST] Saving sample detection..."
    )
    database.save_detection(
        track_id=999,
        label="person",
        confidence=0.95,
        estimated_distance=1.25,
        direction="Center Sector",
        alert_status=True,
        snapshot_path="test_snapshot.jpg"
    )
    print(
        "[TEST] Sample detection saved successfully."
    )
    print(
        "\n[TEST] Saving sample system event..."
    )
    database.save_event(
        event_type="TEST",
        message=(
            "Database manager test event."
        )
    )
    print(
        "[TEST] System event saved successfully."
    )
    print(
        "\n[TEST] Reading recent detections..."
    )
    rows = database.get_recent_detections(
        limit=5
    )
    print("\n" + "=" * 60)
    print(
        "RECENT DETECTIONS"
    )
    print("=" * 60)
    if not rows:
        print(
            "No detection records found."
        )
    else:
        for index, row in enumerate(
            rows,
            start=1
        ):
            (
                timestamp,
                label,
                confidence,
                estimated_distance,
                alert_status
            ) = row
            print(
                f"\nDetection #{index}"
            )
            print(
                f"Timestamp          : {timestamp}"
            )
            print(
                f"Label              : {label}"
            )
            print(
                f"Confidence         : "
                f"{confidence * 100:.2f}%"
            )
            print(
                f"Estimated Distance : "
                f"{estimated_distance:.2f} m"
            )
            print(
                f"Alert Status       : "
                f"{bool(alert_status)}"
            )
    print("\n" + "=" * 60)
    print(
        "[TEST] DATABASE TEST COMPLETED SUCCESSFULLY"
    )
    print("=" * 60)

if __name__ == "__main__":
    main()