"""
model.py - ResNet-50 transfer learning architecture for HCP classification.
Course: AI Developer Expert | Lesson 42

Architecture:
  Backbone  : ResNet-50 pre-trained on ImageNet (frozen in Phase 1)
  Head      : GlobalAvgPool → Dense(512) → Dropout → Dense(256) → Softmax(5)
"""

import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam
from config import IMAGE_SIZE, NUM_CLASSES, LEARNING_RATE, HCP_CLASSES, MODEL_PATH


def build_model(trainable_backbone: bool = False) -> Model:
    """
    Build and compile the ResNet-50 HCP classifier.

    Args:
        trainable_backbone: False = frozen (Phase 1), True = unfrozen (Phase 2).
    Returns:
        Compiled Keras Model.
    """
    # ── ResNet-50 backbone pre-trained on ImageNet ────────────────────────────
    base = ResNet50(
        weights="imagenet",
        include_top=False,            # remove the original 1000-class head
        input_shape=(*IMAGE_SIZE, 3)
    )
    base.trainable = trainable_backbone  # freeze/unfreeze all layers at once

    # ── Custom classification head ────────────────────────────────────────────
    inputs  = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x       = base(inputs, training=False)        # keep BN layers in inference mode
    x       = layers.GlobalAveragePooling2D()(x)
    x       = layers.Dense(512, activation="relu")(x)
    x       = layers.Dropout(0.40)(x)
    x       = layers.Dense(256, activation="relu")(x)
    x       = layers.Dropout(0.30)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = Model(inputs, outputs, name="ResNet50_HCP")
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def unfreeze_top_layers(model: Model, n_layers: int = 30) -> Model:
    """
    Unfreeze the last n_layers of the ResNet-50 backbone for fine-tuning.
    The rest stay frozen to avoid destroying ImageNet features.
    """
    base = model.layers[1]     # ResNet50 sits at index 1
    base.trainable = True
    for layer in base.layers[:-n_layers]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=1e-5),   # very small LR for fine-tuning
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def get_callbacks() -> list:
    """Standard callbacks used in both training phases."""
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5,
            restore_best_weights=True, verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=MODEL_PATH, monitor="val_accuracy",
            save_best_only=True, verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5,
            patience=3, min_lr=1e-8, verbose=1,
        ),
    ]


def print_summary(model: Model):
    """Print a compact model summary with parameter counts."""
    trainable = sum(tf.size(v).numpy() for v in model.trainable_variables)
    total     = sum(tf.size(v).numpy() for v in model.variables)
    print("\n" + "=" * 55)
    print("  ResNet-50  |  HCP Card Classifier")
    print(f"  Input  : {IMAGE_SIZE[0]}×{IMAGE_SIZE[1]}×3")
    print(f"  Output : {NUM_CLASSES} classes → {list(HCP_CLASSES.values())}")
    print(f"  Params : {trainable:,} trainable / {total:,} total")
    print("=" * 55 + "\n")
