"""
============================================================
THREAT ANALYZER
AI-Based Multi-Scope Object Detection and Classification System
============================================================
"""

class ThreatAnalyzer:

    """
    Calculates dynamic threat level based on:

    • Object Category
    • Distance
    • Confidence
    """
    def __init__(self):
        print("[THREAT] Threat Analyzer initialized.")

    def analyze(
        self,
        label,
        distance,
        confidence
    ):

        label = label.lower()
        confidence = confidence * 100
        if label == "person":
            if distance <= 1:
                level = "CRITICAL"
            elif distance <= 2:
                level = "HIGH"
            elif distance <= 4:
                level = "MEDIUM"
            else:
                level = "LOW"
        elif label in {
            "car",
            "bus",
            "truck",
            "motorcycle"
        }:
            if distance <= 2:
                level = "HIGH"
            elif distance <= 5:
                level = "MEDIUM"
            else:
                level = "LOW"
        elif label in {
            "dog",
            "cat",
            "horse",
            "cow",
            "sheep",
            "bird"
        }:
            if distance <= 2:
                level = "MEDIUM"
            else:
                level = "LOW"
        else:
            level = "LOW"
        if confidence < 50:
            level = "LOW"
        color = {
            "CRITICAL": (0, 0, 255),
            "HIGH": (0, 128, 255),
            "MEDIUM": (0, 255, 255),
            "LOW": (0, 255, 0)
        }[level]
        return {
            "level": level,
            "color": color
        }