import json
import os
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import (
    layers,
    models
)

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)

from config import (
    THERMAL_DATASET_DIR,
    THERMAL_IMAGE_WIDTH,
    THERMAL_IMAGE_HEIGHT,
    THERMAL_BATCH_SIZE,
    THERMAL_EPOCHS,
    THERMAL_MODEL_PATH,
    MODELS_DIR,
    REPORTS_DIR
)

VALIDATION_SPLIT = 0.20
RANDOM_SEED = 42
def check_dataset():
    print("=" * 70)
    print(
        "THERMAL CNN TRAINING SYSTEM"
    )
    print("=" * 70)
    print(
        "\n[1/8] Checking thermal dataset..."
    )
    if not os.path.exists(
        THERMAL_DATASET_DIR
    ):
        raise FileNotFoundError(
            "Thermal dataset directory not found:\n"
            f"{THERMAL_DATASET_DIR}"
        )
    class_folders = [
        folder
        for folder in os.listdir(
            THERMAL_DATASET_DIR
        )

        if os.path.isdir(
            os.path.join(
                THERMAL_DATASET_DIR,
                folder
            )
        )
    ]

    class_folders.sort()
    if len(class_folders) < 2:
        raise RuntimeError(
            "At least two class folders are required "
            "inside the thermal dataset directory."
        )
    print(
        "[DATASET] Classes found:"
    )
    for class_name in class_folders:

        class_path = os.path.join(
            THERMAL_DATASET_DIR,
            class_name
        )
        image_count = len(
            [
                filename
                for filename in os.listdir(
                    class_path
                )
                if filename.lower().endswith(
                    (
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".bmp"
                    )
                )
            ]
        )

        print(
            f"  - {class_name}: "
            f"{image_count} images"
        )
    return class_folders
def create_datasets():

    print(
        "\n[2/8] Creating training dataset..."
    )

    training_dataset = (
        tf.keras.utils.image_dataset_from_directory(
            THERMAL_DATASET_DIR,
            validation_split=VALIDATION_SPLIT,
            subset="training",
            seed=RANDOM_SEED,
            image_size=(
                THERMAL_IMAGE_HEIGHT,
                THERMAL_IMAGE_WIDTH
            ),
            batch_size=THERMAL_BATCH_SIZE,
            label_mode="categorical"
        )
    )

    print(
        "\n[3/8] Creating validation dataset..."
    )

    validation_dataset = (
        tf.keras.utils.image_dataset_from_directory(
            THERMAL_DATASET_DIR,
            validation_split=VALIDATION_SPLIT,
            subset="validation",
            seed=RANDOM_SEED,
            image_size=(
                THERMAL_IMAGE_HEIGHT,
                THERMAL_IMAGE_WIDTH
            ),
            batch_size=THERMAL_BATCH_SIZE,
            label_mode="categorical"
        )
    )

    class_names = (
        training_dataset.class_names
    )

    print(
        "\n[DATASET] Class order:"
    )

    for index, class_name in enumerate(
        class_names
    ):

        print(
            f"  {index} -> {class_name}"
        )

    return (
        training_dataset,
        validation_dataset,
        class_names
    )

def optimize_datasets(
    training_dataset,
    validation_dataset
):

    autotune = (
        tf.data.AUTOTUNE
    )

    training_dataset = (
        training_dataset.prefetch(
            buffer_size=autotune
        )
    )

    validation_dataset = (
        validation_dataset.prefetch(
            buffer_size=autotune
        )
    )

    return (
        training_dataset,
        validation_dataset
    )

def create_model(
    number_of_classes
):

    print(
        "\n[4/8] Creating Thermal CNN model..."
    )

    data_augmentation = (
        tf.keras.Sequential(
            [
                layers.RandomFlip(
                    "horizontal"
                ),
                layers.RandomRotation(
                    0.05
                ),
                layers.RandomZoom(
                    0.10
                )
            ],
            name="thermal_data_augmentation"
        )
    )

    model = models.Sequential(

        [

            layers.Input(
                shape=(
                    THERMAL_IMAGE_HEIGHT,
                    THERMAL_IMAGE_WIDTH,
                    3
                )
            ),

            data_augmentation,

            layers.Rescaling(
                1.0 / 255.0
            ),

            layers.Conv2D(
                32,
                kernel_size=3,
                padding="same",
                activation="relu"
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            layers.Conv2D(
                64,
                kernel_size=3,
                padding="same",
                activation="relu"
            ),

            layers.BatchNormalization(),
            layers.MaxPooling2D(),

            layers.Conv2D(
                128,
                kernel_size=3,
                padding="same",
                activation="relu"
            ),

            layers.BatchNormalization(),
            layers.MaxPooling2D(),

            layers.Conv2D(
                256,
                kernel_size=3,
                padding="same",
                activation="relu"
            ),

            layers.BatchNormalization(),
            layers.MaxPooling2D(),
            layers.GlobalAveragePooling2D(),
            layers.Dense(
                128,
                activation="relu"
            ),

            layers.Dropout(
                0.40
            ),

            layers.Dense(
                number_of_classes,
                activation="softmax"
            )
        ]
    )

    model.compile(

        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),

        loss="categorical_crossentropy",

        metrics=[
            "accuracy"
        ]
    )

    print(
        "\n[MODEL] Thermal CNN architecture:"
    )

    model.summary()
    return model

def save_class_names(
    class_names
):

    print(
        "\n[5/8] Saving thermal class names..."
    )

    os.makedirs(
        MODELS_DIR,
        exist_ok=True
    )

    class_file_path = os.path.join(
        MODELS_DIR,
        "thermal_classes.json"
    )

    with open(
        class_file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            class_names,
            file,
            indent=4
        )

    print(
        "[MODEL] Class names saved:"
    )

    print(
        class_file_path
    )

def train_model(
    model,
    training_dataset,
    validation_dataset
):

    print(
        "\n[6/8] Starting CNN training..."
    )

    os.makedirs(
        MODELS_DIR,
        exist_ok=True
    )

    callbacks = [

        ModelCheckpoint(
            filepath=THERMAL_MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),

        EarlyStopping(
            monitor="val_loss",
            patience=7,
            restore_best_weights=True,
            verbose=1
        ),

        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=0.000001,
            verbose=1
        )
    ]

    history = model.fit(
        training_dataset,
        validation_data=validation_dataset,
        epochs=THERMAL_EPOCHS,
        callbacks=callbacks
    )

    return history

def save_final_model(
    model
):

    print(
        "\n[7/8] Saving final Thermal CNN model..."
    )

    model.save(
        THERMAL_MODEL_PATH
    )

    print(
        "[MODEL] Thermal CNN model saved successfully:"
    )

    print(
        THERMAL_MODEL_PATH
    )

def save_training_graphs(
    history
):

    print(
        "\n[8/8] Saving training graphs..."
    )

    os.makedirs(
        REPORTS_DIR,
        exist_ok=True
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        history.history[
            "accuracy"
        ],
        label="Training Accuracy"
    )

    plt.plot(
        history.history[
            "val_accuracy"
        ],
        label="Validation Accuracy"
    )

    plt.title(
        "Thermal CNN Training and Validation Accuracy"
    )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Accuracy"
    )

    plt.legend()

    plt.grid(
        True
    )

    accuracy_graph_path = os.path.join(
        REPORTS_DIR,
        "thermal_cnn_accuracy.png"
    )

    plt.savefig(
        accuracy_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        history.history[
            "loss"
        ],
        label="Training Loss"
    )

    plt.plot(
        history.history[
            "val_loss"
        ],
        label="Validation Loss"
    )

    plt.title(
        "Thermal CNN Training and Validation Loss"
    )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Loss"
    )

    plt.legend()

    plt.grid(
        True
    )

    loss_graph_path = os.path.join(
        REPORTS_DIR,
        "thermal_cnn_loss.png"
    )

    plt.savefig(
        loss_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "[REPORT] Accuracy graph saved:"
    )

    print(
        accuracy_graph_path
    )

    print(
        "[REPORT] Loss graph saved:"
    )

    print(
        loss_graph_path
    )

def main():

    check_dataset()

    (
        training_dataset,
        validation_dataset,
        class_names
    ) = create_datasets()

    (
        training_dataset,
        validation_dataset
    ) = optimize_datasets(
        training_dataset,
        validation_dataset
    )

    save_class_names(
        class_names
    )

    model = create_model(
        number_of_classes=len(
            class_names
        )
    )

    history = train_model(
        model,
        training_dataset,
        validation_dataset
    )

    save_final_model(
        model
    )

    save_training_graphs(
        history
    )

    print("\n" + "=" * 70)
    print(
        "THERMAL CNN TRAINING COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)
    print(
        "\nGenerated Files:"
    )
    print(
        f"1. {THERMAL_MODEL_PATH}"
    )
    print(
        "2. "
        + os.path.join(
            MODELS_DIR,
            "thermal_classes.json"
        )
    )
    print(
        "3. "
        + os.path.join(
            REPORTS_DIR,
            "thermal_cnn_accuracy.png"
        )
    )
    print(
        "4. "
        + os.path.join(
            REPORTS_DIR,
            "thermal_cnn_loss.png"
        )
    )
if __name__ == "__main__":
    main()