import os
from datetime import datetime
import cv2
from config import (
    EVIDENCE_DIR
)

class EvidenceManager:
    """
    Manages detection and alert evidence snapshots.
    """
    def __init__(self):

        self.evidence_dir = (
            EVIDENCE_DIR
        )
        os.makedirs(
            self.evidence_dir,
            exist_ok=True
        )
        print(
            "[EVIDENCE] Evidence Manager initialized."
        )

    def save_snapshot(
        self,
        frame,
        track_id,
        label,
        prefix="alert"
    ):

        if frame is None:

            raise ValueError(
                "Cannot save an empty frame."
            )

        timestamp = (
            datetime.now().strftime(
                "%Y%m%d_%H%M%S_%f"
            )
        )

        safe_label = (
            str(label)
            .lower()
            .strip()
            .replace(" ", "_")
        )

        filename = (
            f"{prefix}_"
            f"{track_id}_"
            f"{safe_label}_"
            f"{timestamp}.jpg"
        )

        file_path = os.path.join(
            self.evidence_dir,
            filename
        )

        success = cv2.imwrite(
            file_path,
            frame
        )
        if not success:

            raise RuntimeError(
                "Failed to save evidence snapshot."
            )

        print(
            f"[EVIDENCE] Snapshot saved: "
            f"{file_path}"
        )
        return file_path

    def get_evidence_count(self):

        if not os.path.exists(
            self.evidence_dir
        ):
            return 0

        supported_extensions = (
            ".jpg",
            ".jpeg",
            ".png"
        )

        files = [
            filename

            for filename in os.listdir(
                self.evidence_dir
            )

            if filename.lower().endswith(
                supported_extensions
            )
        ]
        return len(
            files
        )

    def get_recent_evidence(
        self,
        limit=10
    ):
        if not os.path.exists(
            self.evidence_dir
        ):
            return []
        files = []

        for filename in os.listdir(
            self.evidence_dir
        ):
            file_path = os.path.join(
                self.evidence_dir,
                filename
            )
            if os.path.isfile(
                file_path
            ):
                files.append(
                    (
                        file_path,
                        os.path.getmtime(
                            file_path
                        )
                    )
                )
        files.sort(
            key=lambda item: item[1],
            reverse=True
        )
        return [
            file_path

            for file_path, _ in files[
                :limit
            ]
        ]