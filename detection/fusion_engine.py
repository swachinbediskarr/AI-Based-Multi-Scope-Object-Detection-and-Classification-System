class FusionEngine:
    """
    Combines RGB YOLO detection results with
    Thermal CNN classification results.
    """

    def __init__(
        self,
        rgb_weight=0.60,
        thermal_weight=0.40
    ):
        self.rgb_weight = rgb_weight
        self.thermal_weight = thermal_weight
        self.class_mapping = {
    
            "person": "human",
            "human": "human",
            "children": "children",

            "car": "vehicle",
            "motorcycle": "vehicle",
            "bus": "vehicle",
            "truck": "vehicle",
            "vehicle": "vehicle",
            "helmet": "helmet",
            "glass": "glass",
            "bat": "bat",
            "ball": "ball",

            "dog": "animal",
            "cat": "animal",
            "horse": "animal",
            "cow": "animal",
            "sheep": "animal",
            "bird": "animal",
            "animal": "animal",
            "tiger": "tiger",
            "lion": "lion",
            "elephant": "elephant",
        }

    def normalize_class(self, class_name):
        if class_name is None:
            return None
        class_name = class_name.lower().strip()
        return self.class_mapping.get(
            class_name,
            class_name
        )

    def fuse(
        self,
        rgb_result=None,
        thermal_result=None
    ):
        if rgb_result is None and thermal_result is None:
            return {
                "status": "NO_DETECTION",
                "final_class": None,
                "confidence": 0.0,
                "agreement": False,
                "source": "None"
            }

        if thermal_result is None:
            rgb_class = self.normalize_class(
                rgb_result["label"]
            )

            return {
                "status": "RGB_ONLY",
                "rgb_class": rgb_class,
                "rgb_confidence": rgb_result["confidence"],
                "thermal_class": None,
                "thermal_confidence": 0.0,
                "final_class": rgb_class,
                "confidence": rgb_result["confidence"],
                "agreement": False,
                "source": "RGB YOLO"
            }

        if rgb_result is None:

            thermal_class = self.normalize_class(
                thermal_result["class"]
            )

            return {
                "status": "THERMAL_ONLY",
                "rgb_class": None,
                "rgb_confidence": 0.0,
                "thermal_class": thermal_class,
                "thermal_confidence": thermal_result["confidence"],
                "final_class": thermal_class,
                "confidence": thermal_result["confidence"],
                "agreement": False,
                "source": "Thermal CNN"
            }

        rgb_class = self.normalize_class(
            rgb_result["label"]
        )

        thermal_class = self.normalize_class(
            thermal_result["class"]
        )

        rgb_confidence = float(
            rgb_result["confidence"]
        )

        thermal_confidence = float(
            thermal_result["confidence"]
        )

        if rgb_class == thermal_class:

            fusion_confidence = (
                rgb_confidence * self.rgb_weight
                +
                thermal_confidence * self.thermal_weight
            )

            return {
                "status": "CONFIRMED",
                "rgb_class": rgb_class,
                "rgb_confidence": rgb_confidence,
                "thermal_class": thermal_class,
                "thermal_confidence": thermal_confidence,
                "final_class": rgb_class,
                "confidence": fusion_confidence,
                "agreement": True,
                "source": "RGB + Thermal Fusion"
            }

        rgb_weighted_score = (
            rgb_confidence * self.rgb_weight
        )

        thermal_weighted_score = (
            thermal_confidence * self.thermal_weight
        )

        if rgb_weighted_score >= thermal_weighted_score:

            final_class = rgb_class
            final_confidence = rgb_confidence
            winning_source = "RGB YOLO"

        else:

            final_class = thermal_class
            final_confidence = thermal_confidence
            winning_source = "Thermal CNN"

        return {
            "status": "CONFLICT",
            "rgb_class": rgb_class,
            "rgb_confidence": rgb_confidence,
            "thermal_class": thermal_class,
            "thermal_confidence": thermal_confidence,
            "final_class": final_class,
            "confidence": final_confidence,
            "agreement": False,
            "source": winning_source
        }