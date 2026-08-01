from detection.fusion_engine import FusionEngine
def main():
    print("=" * 60)
    print("RGB + THERMAL FUSION ENGINE TEST")
    print("=" * 60)
    fusion_engine = FusionEngine(
        rgb_weight=0.60,
        thermal_weight=0.40
    )

    rgb_result = {
        "label": "person",
        "confidence": 0.94
    }

    thermal_result = {
        "class": "human",
        "confidence": 0.91
    }

    result = fusion_engine.fuse(
        rgb_result=rgb_result,
        thermal_result=thermal_result
    )

    print("\nRGB YOLO RESULT")
    print("-" * 40)
    print("Class      :", rgb_result["label"])
    print(
        "Confidence :",
        f"{rgb_result['confidence'] * 100:.2f}%"
    )

    print("\nTHERMAL CNN RESULT")
    print("-" * 40)
    print("Class      :", thermal_result["class"])
    print(
        "Confidence :",
        f"{thermal_result['confidence'] * 100:.2f}%"
    )

    print("\nFINAL FUSION RESULT")
    print("-" * 40)
    print("Status     :", result["status"])
    print("Final Class:", result["final_class"])
    print(
        "Confidence :",
        f"{result['confidence'] * 100:.2f}%"
    )
    print("Agreement  :", result["agreement"])
    print("Source     :", result["source"])

if __name__ == "__main__":
    main()