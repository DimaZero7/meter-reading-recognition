import os
import shutil
from pathlib import Path
from typing import Union

import imagehash
import pandas as pd
from PIL import Image
from django.conf import settings
from django.db.models import QuerySet

from apps.data.models import Training, TrainingElement
from django.core.files import File


def import_training_data() -> None:
    """
    Imports training data from a CSV file, creates Training model instances with associated images, and saves them
        in bulk to the database.
    """
    data_frame = pd.read_csv(settings.IMPORT_TRAINING_CSV_PATH)
    to_create = []

    for index, row in data_frame.iterrows():
        image_path = Path(settings.IMPORT_TRAINING_IMAGE_PATH) / row['image']
        image_file = File(open(image_path, 'rb'))

        instance = Training(type=row['type'], correct_value=row['correct_value'], image=image_file)

        to_create.append(instance)
    Training.objects.bulk_create(to_create)

    print(f'The training sample has been successfully uploaded.')


def duplicate_removal():
    trainings = Training.objects.all().only('image', 'correct_value')

    training_hashes = {}
    for iteration, training in enumerate(trainings):
        print(f"{iteration + 1}/{len(trainings)}")

        with Image.open(training.image.path) as img:
            hash = str(imagehash.average_hash(img))

        if hash in training_hashes and training_hashes[hash].correct_value == training.correct_value:
            training.delete()
        else:
            training_hashes[hash] = training

    print('Duplicates successfully deleted')
