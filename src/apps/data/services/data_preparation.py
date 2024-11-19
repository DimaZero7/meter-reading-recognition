from typing import Union, Tuple, Optional

import numpy as np
import pandas as pd
from django.conf import settings
from django.db.models import QuerySet
from keras.preprocessing.image import img_to_array, load_img
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.utils import Sequence

from apps.data.choices import TrainingType
from apps.data.models import Training, TrainingAugmentation
from apps.neural_net.services.output import convert_float_to_categorical


class CustomDataGenerator(Sequence):
    """
    CustomDataGenerator is a custom data generator used for creating batches of images and their corresponding values
    for training, testing, and validating a neural network.

    This class takes a DataFrame with image paths and their values, applies specified transformations to the images,
    and converts numerical values into a categorical format.
    """
    def __init__(
        self,
        dataframe: pd.DataFrame,
        datagen: ImageDataGenerator,
        target_size: Tuple[int, int] = (settings.IMAGE_SIZE_X, settings.IMAGE_SIZE_Y),
        batch_size: int = 32,
    ):
        super().__init__()
        self.dataframe = dataframe
        self.datagen = datagen
        self.target_size = target_size
        self.batch_size = batch_size

    def __len__(self):
        """Returns the number of batches per epoch"""
        return int(np.ceil(len(self.dataframe) / self.batch_size))

    def __getitem__(self, index):
        """Generation of a single data batch"""
        batch_slice = slice(index * self.batch_size, (index + 1) * self.batch_size)
        batch_records  = self.dataframe.iloc[batch_slice].to_dict('records')
        images = np.array([self.load_image(record['image']) for record in batch_records])
        labels = np.array([convert_float_to_categorical(record['correct_value']) for record in batch_records])
        return images, labels

    def load_image(self, path):
        """Image loading and augmentation"""
        img = load_img(path, target_size=self.target_size)
        img = img_to_array(img)
        img = self.datagen.random_transform(img)
        img = self.datagen.standardize(img)
        return img


class DataPreparation:
    def _convert_data_frame(self, queryset: Union[QuerySet[Training], QuerySet[TrainingAugmentation]]) -> pd.DataFrame:
        data_list = []
        for obj in queryset:
            data_list.append({
                'image': obj.image.path,
                'type': obj.type,
                'correct_value': obj.correct_value
            })

        data_frame = pd.DataFrame(data_list)

        return data_frame

    def get_training_data(self) -> pd.DataFrame:
        trainings = Training.objects.all().only('id', 'image', 'type', 'correct_value')
        data_frame = self._convert_data_frame(queryset=trainings)
        return data_frame

    def get_training_augmentation_data(self) -> pd.DataFrame:
        trainings_aug = TrainingAugmentation.objects.all().only('id', 'image', 'type', 'correct_value')
        data_frame = self._convert_data_frame(queryset=trainings_aug)
        return data_frame

    def get_union_training_and_training_augmentation(self) -> pd.DataFrame:
        data_frame_training = self.get_training_data()
        data_frame_training_aug = self.get_training_augmentation_data()
        data_frame_union = pd.concat([data_frame_training, data_frame_training_aug], ignore_index=True)
        return data_frame_union

    def get_image_generators(self, batch_size: Optional[int] = 32) -> Tuple[Sequence, Sequence, Sequence]:
        """
        This method creates and returns data generators for training, testing, and validation image datasets.

        How is it?
        - The method retrieves a combined dataset and splits it into training, testing, and validation sets based
            on type.
        - It sets up data augmentation for the training set using `ImageDataGenerator` to apply random transformations.
        - It creates custom data generators for each set with specific configurations.
        - Finally, it returns the generators for use in model training and evaluation.

        Returns:
            Tuple[Sequence, Sequence, Sequence]: A tuple containing the training, testing, and validation data
                generators.
        """
        dataset = self.get_union_training_and_training_augmentation()

        training_set = dataset[dataset["type"] == TrainingType.TEACH.value]
        testing_set = dataset[dataset["type"] == TrainingType.TEST.value]
        validation_set = dataset[dataset["type"] == TrainingType.VALIDATE.value]
        del dataset

        training_generator = ImageDataGenerator(
            rotation_range=0.1,
            rescale=1.0 / 255,
            shear_range=0.5,
            zoom_range=0.1,
            horizontal_flip=False,
            width_shift_range=0.05,
            height_shift_range=0.05,
            brightness_range=[0.6, 1.4],
        )
        training_generator = CustomDataGenerator(
            training_set,
            training_generator,
            batch_size=batch_size,
        )

        test_datagen = ImageDataGenerator(rescale=1.0 / 255)
        test_generator = CustomDataGenerator(
            testing_set,
            test_datagen,
            batch_size=1,
        )

        validation_datagen = ImageDataGenerator(rescale=1.0 / 255)
        validation_generator = CustomDataGenerator(
            validation_set,
            validation_datagen,
            batch_size=1,
        )

        return training_generator, test_generator, validation_generator
