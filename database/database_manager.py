import sqlite3
from datetime import datetime
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.database_path = DATABASE_PATH

        self.initialize_database()

    def initialize_database(self):

        connection = sqlite3.connect(
            self.database_path
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detections
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                track_id INTEGER,

                label TEXT,

                confidence REAL,

                estimated_distance REAL,

                direction TEXT,

                alert_status INTEGER,

                snapshot_path TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_events
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                message TEXT
            )
            """
        )

        connection.commit()

        connection.close()

        print(
            "[DATABASE] Database initialized successfully."
        )

    def save_detection(
        self,
        track_id,
        label,
        confidence,
        estimated_distance,
        direction,
        alert_status,
        snapshot_path=""
    ):
        connection = sqlite3.connect(
            self.database_path
        )

        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO detections
            (
                timestamp,
                track_id,
                label,
                confidence,
                estimated_distance,
                direction,
                alert_status,
                snapshot_path
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (
                timestamp,
                track_id,
                label,
                confidence,
                estimated_distance,
                direction,
                int(alert_status),
                snapshot_path
            )
        )

        connection.commit()
        connection.close()
    def save_event(
        self,
        event_type,
        message
    ):

        connection = sqlite3.connect(
            self.database_path
        )
        cursor = connection.cursor()
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        cursor.execute(
            """
            INSERT INTO system_events
            (
                timestamp,
                event_type,
                message
            )

            VALUES (?, ?, ?)
            """,

            (
                timestamp,
                event_type,
                message
            )
        )

        connection.commit()
        connection.close()

    def get_recent_detections(
        self,
        limit=10
    ):
        connection = sqlite3.connect(
            self.database_path
        )
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                timestamp,
                label,
                confidence,
                estimated_distance,
                alert_status

            FROM detections

            ORDER BY id DESC

            LIMIT ?
            """,

            (limit,)
        )

        rows = cursor.fetchall()
        connection.close()
        return rows