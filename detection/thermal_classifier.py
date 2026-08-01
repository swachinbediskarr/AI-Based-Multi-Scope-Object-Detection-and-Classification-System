import json
import os
import cv2
import numpy as np
import tensorflow as tf

from config import (
    THERMAL_MODEL_PATH,
    THERMAL_IMAGE_WIDTH,
    THERMAL_IMAGE_HEIGHT,
    MODELS_DIR
)

class ThermalClassifier:

    def __init__(self):

        print(
            "[THERMAL AI] Initializing Thermal CNN..."
        )

        self.model = None

        self.class_names = [
            "animal",
            "human",
            "vehicle"
        ]

        class_file = os.path.join(
            MODELS_DIR,
            "thermal_classes.json"
        )

        if os.path.exists(
            class_file
        ):

            with open(
                class_file,
                "r",
                encoding="utf-8"
            ) as file:

                self.class_names = (
                    json.load(
                        file
                    )
                )

            print(
                "[THERMAL AI] Class names loaded."
            )

        else:

            print(
                "[THERMAL AI] Class file not found."
            )

            print(
                "[THERMAL AI] Using default classes:",
                self.class_names
            )

        print(
            "[THERMAL AI] Expected model path:"
        )

        print(
            THERMAL_MODEL_PATH
        )

        if os.path.exists(
            THERMAL_MODEL_PATH
        ):
            try:
                self.model = (
                    tf.keras.models.load_model(
                        THERMAL_MODEL_PATH
                    )
                )
                print(
                    "[THERMAL AI] CNN model "
                    "loaded successfully."
                )
            except Exception as error:

                print(
                    "[THERMAL AI] Model loading failed:"
                )
                print(
                    error
                )
                print(
                    "[THERMAL AI] Running in DEMO mode."
                )
                self.model = None
        else:

            print(
                "[THERMAL AI] CNN model not found."
            )

            print(
                "[THERMAL AI] Running in DEMO mode."
            )

    def classify(
        self,
        thermal_image
    ):

        if thermal_image is None:

            return {
                "success": False,
                "class": None,
                "confidence": 0.0,
                "message": (
                    "Thermal image is empty."
                )
            }

        if self.model is None:

            return {
                "success": True,
                "class": "human",
                "confidence": 0.75,
                "confidence_percentage": 75.0,
                "all_probabilities": [
                    0.10,
                    0.75,
                    0.15
                ],
                "mode": "DEMO"
            }

        image = cv2.resize(
            thermal_image,
            (
                THERMAL_IMAGE_WIDTH,
                THERMAL_IMAGE_HEIGHT
            )
        )
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )
        image = image.astype(
            np.float32
        )

        image = np.expand_dims(
            image,
            axis=0
        )
        predictions = (
            self.model.predict(
                image,
                verbose=0
            )[0]
        )
        class_index = int(
            np.argmax(
                predictions
            )
        )
        class_name = (
            self.class_names[
                class_index
            ]
        )
        confidence = float(
            predictions[
                class_index
            ]
        )

        return {
            "success": True,
            "class": class_name,
            "confidence": confidence,
            "confidence_percentage":
                confidence * 100,
            "all_probabilities":
                predictions.tolist(),
            "mode": "CNN"
        }