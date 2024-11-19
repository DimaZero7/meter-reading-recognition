import os
import shutil
import tempfile
from io import BytesIO
from typing import Optional

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from keras import Sequential
from keras import layers
from keras.src.optimizers import Adam
from keras.utils import Sequence
from keras.models import load_model
import tensorflow as tf

from apps.neural_net.models import NeuralModel, NeuralVersion
from apps.neural_net.services.output import convert_float_to_categorical, convert_categorical_to_number, \
    compare_numbers


class ModelManager:
    def __init__(self, model_name: Optional[str] = None):
        if model_name:
            model = NeuralModel.objects.get(name=model_name)
            last_version = self.get_model_last_version(model_id=model.id)
            model_file_path = last_version.model.path
            model = load_model(model_file_path)
            self.model = model
        else:
            self.create_and_compile_model()

    def get_model_last_version(self, model_id: int) -> NeuralVersion:
        return NeuralVersion.objects.filter(neural_model_id=model_id).order_by('version').last()

    def compile_model(self) -> None:
        self.model.compile(
            loss="categorical_crossentropy",
            optimizer=Adam(learning_rate=0.0001),
            metrics=["accuracy"],
        )

    def create_and_compile_model(self) -> None:
        self.model = Sequential()
        self.model.add(
            layers.Input(
                shape=(settings.IMAGE_SIZE_X, settings.IMAGE_SIZE_Y, settings.IMAGE_SIZE_Z)
            )
        )

        self.model.add(layers.Conv2D(16, 2, activation="elu", padding="same"))
        self.model.add(layers.Conv2D(16, 3, activation="elu", padding="same"))
        self.model.add(layers.MaxPooling2D(2))

        self.model.add(layers.Conv2D(32, 2, activation="elu", padding="same"))
        self.model.add(layers.Conv2D(32, 3, activation="elu", padding="same"))
        self.model.add(layers.MaxPooling2D(2))

        self.model.add(layers.Conv2D(64, 2, activation="elu", padding="same"))
        self.model.add(layers.Conv2D(64, 3, activation="elu", padding="same"))
        self.model.add(layers.MaxPooling2D(2))

        self.model.add(layers.Conv2D(128, 2, activation="elu", padding="same"))
        self.model.add(layers.Conv2D(128, 3, activation="elu", padding="same"))
        self.model.add(layers.MaxPooling2D(2))

        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(units=512, activation="elu"))

        self.model.add(layers.Dense(units=110))
        self.model.add(layers.Reshape((11, 10)))
        self.model.add(layers.Activation("softmax"))
        self.model.summary()

        self.compile_model()

    def start_training(self, training_generator: Sequence, test_generator: Sequence, epochs: int) -> None:
        self.compile_model()
        self.model.fit(
            training_generator,
            epochs=epochs,
            validation_data=test_generator,
        )

    def accuracy_check(self, validation_generator: Sequence) -> dict:
        """
        Checks the accuracy of the model's predictions on validation data and returns mismatch statistics.

        Returns:
        --------
        dict
            A dictionary where the keys represent the number of mismatches between the predicted and correct values,
            and the values are lists containing the count and its percentage.

        Example output:
        ---------------
        {"3": [2, "10.53%"], "4": [17, "89.47%"]}  # Number of mismatches and their percentage.
        """
        predictions = self.model.predict(validation_generator,
                                         steps=len(validation_generator))

        correct_values = [
            convert_categorical_to_number(convert_float_to_categorical(value))
            for value in validation_generator.dataframe["correct_value"]
        ]

        stats = {}

        for prediction, correct_value in zip(predictions, correct_values):
            predicted_number = convert_categorical_to_number(prediction)

            number_mismatches = compare_numbers(correct_value,
                                                predicted_number)
            if number_mismatches in stats:
                stats[number_mismatches] += 1
            else:
                stats[number_mismatches] = 1

        total_samples = sum(stats.values())

        stats_with_percentage = {}
        for key, count in stats.items():
            percentage = (count / total_samples) * 100
            stats_with_percentage[str(key)] = [count, f"{percentage:.2f}%"]

        return stats_with_percentage

    @transaction.atomic
    def save(self, model_name: str, validation_generator: Sequence, changes: Optional[str] = None) -> None:
        structure_data = [
            {"name": layer.name, "type": layer.__class__.__name__, "config": layer.get_config()}
            for layer in self.model.layers
        ]
        neural_model, created = NeuralModel.objects.get_or_create(
            name=model_name,
            defaults={'structure': structure_data}
        )

        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as temp_model_file:
            self.model.save(temp_model_file.name)
            temp_model_file.seek(0)
            model_buffer = BytesIO(temp_model_file.read())

        export_dir = "tflite_models"
        self.model.export(export_dir)
        converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
        tflite_model = converter.convert()
        tflite_model_buffer = BytesIO(tflite_model)
        if os.path.exists(export_dir):
            shutil.rmtree(export_dir)

        stats = self.accuracy_check(validation_generator=validation_generator)

        if created:
            NeuralVersion.objects.create(
                neural_model=neural_model,
                version=1,
                changes="First version",
                model=ContentFile(model_buffer.read(), name=f'{model_name}.h5'),
                tflite_model=ContentFile(tflite_model_buffer.getvalue(), name=f'{model_name}.tflite'),
                stats=stats,
            )
        else:
            last_version = self.get_model_last_version(model_id=neural_model.id)
            NeuralVersion.objects.create(
                neural_model=neural_model,
                version=last_version.version + 1,
                changes=changes,
                model=ContentFile(model_buffer.read(), name=f'{model_name}.h5'),
                tflite_model=ContentFile(tflite_model_buffer.getvalue(), name=f'{model_name}.tflite'),
                stats=stats,
            )

        os.remove(temp_model_file.name)
