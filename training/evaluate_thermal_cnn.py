import os
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from config import (
    THERMAL_DATASET_DIR,
    THERMAL_MODEL_PATH,
    THERMAL_IMAGE_WIDTH,
    THERMAL_IMAGE_HEIGHT,
    THERMAL_BATCH_SIZE,
    REPORTS_DIR,
    MODELS_DIR
)

TEST_DIR = os.path.join(
    THERMAL_DATASET_DIR,
    "test"
)

CLASS_NAMES_PATH = os.path.join(
    MODELS_DIR,
    "thermal_classes.json"
)

with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:

    class_names = json.load(
        file
    )

test_dataset = tf.keras.utils.image_dataset_from_directory(

    TEST_DIR,

    image_size=(
        THERMAL_IMAGE_HEIGHT,
        THERMAL_IMAGE_WIDTH
    ),
    batch_size=THERMAL_BATCH_SIZE,
    label_mode="categorical",
    shuffle=False
)

model = tf.keras.models.load_model(
    THERMAL_MODEL_PATH
)
test_loss, test_accuracy = model.evaluate(
    test_dataset
)
print(
    "\nTest Accuracy:",
    test_accuracy
)

print(
    "Test Loss:",
    test_loss
)
predictions = model.predict(
    test_dataset
)
predicted_labels = np.argmax(
    predictions,
    axis=1
)
true_labels = np.concatenate(
    [
        np.argmax(
            labels.numpy(),
            axis=1
        )

        for images, labels
        in test_dataset
    ]
)

report = classification_report(
    true_labels,
    predicted_labels,
    target_names=class_names
)

print(
    "\nClassification Report:\n"
)

print(
    report
)

report_path = os.path.join(
    REPORTS_DIR,
    "thermal_classification_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        report
    )

matrix = confusion_matrix(
    true_labels,
    predicted_labels
)

display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=class_names
)

display.plot()

plt.title(
    "Thermal CNN Confusion Matrix"
)
confusion_matrix_path = os.path.join(
    REPORTS_DIR,
    "thermal_confusion_matrix.png"
)
plt.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)
plt.close()
print(
    "\nEvaluation completed successfully."
)