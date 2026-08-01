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
from analytics.analytics_manager import (
    AnalyticsManager
)
from evidence.evidence_manager import (
    EvidenceManager
)
from gui.dashboard import (
    Dashboard
)
def main():
    print("=" * 70)
    print(
        "AI-BASED MULTI-SCOPE OBJECT "
        "DETECTION AND CLASSIFICATION SYSTEM"
    )
    print("=" * 70)
    print(
        "\nStarting system initialization..."
    )
    print(
        "\n[1/8] Initializing RGB YOLO Engine..."
    )
    detector = (
        YOLODetector()
    )
    print(
        "[1/8] RGB YOLO Engine initialized successfully."
    )
    print(
        "\n[2/8] Initializing Thermal CNN Engine..."
    )
    thermal_classifier = (
        ThermalClassifier()
    )
    print(
        "[2/8] Thermal CNN Engine initialized successfully."
    )
    print(
        "\n[3/8] Initializing Fusion Engine..."
    )
    fusion_engine = (
        FusionEngine(
            rgb_weight=0.60,
            thermal_weight=0.40
        )
    )
    print(
        "[3/8] Fusion Engine initialized successfully."
    )
    print(
        "\n[4/8] Initializing Database Manager..."
    )
    database = (
        DatabaseManager()
    )
    print(
        "[4/8] Database Manager initialized successfully."
    )
    print(
        "\n[5/8] Initializing Alert Manager..."
    )
    alert_manager = (
        AlertManager()
    )
    print(
        "[5/8] Alert Manager initialized successfully."
    )
    print(
        "\n[6/8] Initializing Report Generator..."
    )
    report_generator = (
        ReportGenerator()
    )
    print(
        "[6/8] Report Generator initialized successfully."
    )
    print(
        "\n[7/8] Initializing Evidence Manager..."
    )
    evidence_manager = (
        EvidenceManager()
    )
    print(
        "[7/8] Evidence Manager initialized successfully."
    )
    print(
        "\n[8/8] Initializing Analytics Manager..."
    )
    analytics_manager = (
        AnalyticsManager()
    )
    print(
        "[8/8] Analytics Manager initialized successfully."
    )
    print("\n" + "=" * 70)
    print(
        "ALL SYSTEM MODULES INITIALIZED SUCCESSFULLY"
    )
    print("=" * 70)
    print(
        "\n[DASHBOARD] Starting AI monitoring dashboard..."
    )
    dashboard = (
        Dashboard(
            detector=detector,
            thermal_classifier=thermal_classifier,
            fusion_engine=fusion_engine,
            database=database,
            alert_manager=alert_manager,
            report_generator=report_generator,
            evidence_manager=evidence_manager,
            analytics_manager=analytics_manager
        )
    )
    dashboard.run()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\n[SYSTEM] Application stopped by user."
        )
    except Exception as error:
        print("\n" + "=" * 70)
        print(
            "[SYSTEM ERROR]"
        )
        print(
            f"{type(error).__name__}: "
            f"{error}"
        )
        print("=" * 70)
        raise