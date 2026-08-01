import time
from alerts.alert_manager import (
    AlertManager
)

def main():

    print("=" * 60)
    print(
        "ALERT MANAGER TEST"
    )

    print("=" * 60)
    print(
        "\n[TEST] Initializing Alert Manager..."
    )

    alert_manager = AlertManager()

    print(
        "[TEST] Alert Manager initialized successfully."
    )
    print(
        f"\nVoice Enabled : "
        f"{alert_manager.voice_enabled}"
    )
    print(
        f"Alert Cooldown: "
        f"{alert_manager.alert_cooldown} seconds"
    )
    print(
        "\n[TEST] Testing alert cooldown..."
    )
    test_track_id = 999
    first_alert = alert_manager.can_alert(
        test_track_id
    )
    print(
        f"First alert allowed : "
        f"{first_alert}"
    )
    second_alert = alert_manager.can_alert(
        test_track_id
    )
    print(
        f"Immediate second alert allowed : "
        f"{second_alert}"
    )
    if (
        first_alert is True
        and
        second_alert is False
    ):
        print(
            "[PASS] Cooldown mechanism is working."
        )
    else:
        print(
            "[FAIL] Cooldown mechanism is not working correctly."
        )
    print(
        f"\n[TEST] Waiting "
        f"{alert_manager.alert_cooldown} seconds "
        f"for cooldown..."
    )

    time.sleep(
        alert_manager.alert_cooldown
        +
        1
    )
    third_alert = alert_manager.can_alert(
        test_track_id
    )
    print(
        f"Alert after cooldown allowed : "
        f"{third_alert}"
    )
    if third_alert:
        print(
            "[PASS] Alert allowed after cooldown."
        )
    else:
        print(
            "[FAIL] Alert still blocked after cooldown."
        )
    print(
        "\n[TEST] Testing voice alert..."
    )
    alert_manager.speak(
        "This is a test alert from the "
        "AI based multi scope object "
        "detection and classification system."
    )
    time.sleep(5)
    print(
        "\n[TEST] Testing voice toggle..."
    )
    previous_state = (
        alert_manager.voice_enabled
    )
    new_state = (
        alert_manager.toggle_voice()
    )
    print(
        f"Previous Voice State : "
        f"{previous_state}"
    )
    print(
        f"New Voice State      : "
        f"{new_state}"
    )
    if (
        previous_state
        !=
        new_state
    ):
        print(
            "[PASS] Voice toggle is working."
        )
    else:
        print(
            "[FAIL] Voice toggle test failed."
        )
    if (
        alert_manager.voice_enabled
        !=
        previous_state
    ):
        alert_manager.toggle_voice()
    print(
        "\n[TEST] Original voice state restored."
    )
    print("\n" + "=" * 60)
    print(
        "[TEST] ALERT MANAGER TEST COMPLETED"
    )
    print("=" * 60)

if __name__ == "__main__":
    main()