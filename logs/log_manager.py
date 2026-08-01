import logging
import os
from datetime import datetime
from config import LOGS_DIR

class LogManager:

    """
    Central logging manager for the complete AI-based
    multi-scope object detection and classification system.

    This manager maintains separate log files for:

    1. System events
    2. Object detections
    3. Security alerts
    4. Application errors
    """

    def __init__(self):

        print(
            "[LOG] Initializing Log Manager..."
        )

        os.makedirs(
            LOGS_DIR,
            exist_ok=True
        )

        self.system_log_path = os.path.join(
            LOGS_DIR,
            "system.log"
        )

        self.detection_log_path = os.path.join(
            LOGS_DIR,
            "detection.log"
        )

        self.alert_log_path = os.path.join(
            LOGS_DIR,
            "alert.log"
        )

        self.error_log_path = os.path.join(
            LOGS_DIR,
            "error.log"
        )

        self.system_logger = self._create_logger(
            logger_name="AI_SYSTEM_LOGGER",
            file_path=self.system_log_path,
            level=logging.INFO
        )

        self.detection_logger = self._create_logger(
            logger_name="AI_DETECTION_LOGGER",
            file_path=self.detection_log_path,
            level=logging.INFO
        )

        self.alert_logger = self._create_logger(
            logger_name="AI_ALERT_LOGGER",
            file_path=self.alert_log_path,
            level=logging.WARNING
        )

        self.error_logger = self._create_logger(
            logger_name="AI_ERROR_LOGGER",
            file_path=self.error_log_path,
            level=logging.ERROR
        )

        self.log_system(
            "Log Manager initialized successfully."
        )

        print(
            "[LOG] Log Manager initialized successfully."
        )

    def _create_logger(
        self,
        logger_name,
        file_path,
        level
    ):

        logger = logging.getLogger(
            logger_name
        )

        logger.setLevel(
            level
        )
        logger.propagate = False
        if logger.handlers:
            logger.handlers.clear()

        file_handler = logging.FileHandler(
            file_path,
            mode="a",
            encoding="utf-8"
        )

        file_handler.setLevel(
            level
        )

        formatter = logging.Formatter(

            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

        return logger

    def log_system(
        self,
        message
    ):

        self.system_logger.info(
            str(
                message
            )
        )

    def log_detection(
        self,
        track_id,
        label,
        confidence,
        estimated_distance=None,
        direction=None
    ):
        if confidence is None:
            confidence = 0.0

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):
            confidence = 0.0
        if estimated_distance is None:
            distance_text = "N/A"
        else:
            try:
                distance_text = (
                    f"{float(estimated_distance):.2f} m"
                )

            except (
                TypeError,
                ValueError
            ):
                distance_text = "N/A"
        if direction is None:
            direction = "UNKNOWN"

        message = (
            f"Track ID: {track_id} | "
            f"Label: {label} | "
            f"Confidence: "
            f"{confidence * 100:.2f}% | "
            f"Distance: {distance_text} | "
            f"Direction: {direction}"
        )

        self.detection_logger.info(
            message
        )

    def log_alert(
        self,
        message,
        track_id=None,
        label=None
    ):

        alert_message = (
            str(
                message
            )
        )

        if track_id is not None:
            alert_message += (
                f" | Track ID: "
                f"{track_id}"
            )
        if label is not None:
            alert_message += (
                f" | Object: "
                f"{label}"
            )

        self.alert_logger.warning(
            alert_message
        )

    def log_error(
        self,
        message,
        exception=None
    ):

        error_message = (
            str(
                message
            )
        )

        if exception is not None:

            error_message += (
                f" | Exception: "
                f"{type(exception).__name__}: "
                f"{exception}"
            )

        self.error_logger.error(
            error_message
        )

    def log_session_start(
        self
    ):

        separator = (
            "=" * 60
        )

        self.log_system(
            separator
        )

        self.log_system(
            "NEW APPLICATION SESSION STARTED"
        )

        self.log_system(
            f"Session Time: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        self.log_system(
            separator
        )

    def log_session_end(
        self
    ):

        separator = (
            "=" * 60
        )

        self.log_system(
            separator
        )

        self.log_system(
            "APPLICATION SESSION ENDED"
        )

        self.log_system(
            f"Session Time: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        self.log_system(
            separator
        )

    def get_log_paths(
        self
    ):
        return {
            "system":
                self.system_log_path,

            "detection":
                self.detection_log_path,

            "alert":
                self.alert_log_path,

            "error":
                self.error_log_path
        }