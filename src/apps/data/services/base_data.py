import os
import shutil
from pathlib import Path
from typing import Union

import pandas as pd
from django.conf import settings
from django.db.models import QuerySet

from apps.data.models import Training, TrainingElement
from django.core.files import File


def create_base_dataset(queryset: Union[QuerySet[Training], QuerySet[TrainingElement]], fields: list[str], csv_path: str) -> None:
    """
    Processes a set of Training models or TrainingElement to create a CSV file with the specified fields as well as
        it copies the associated image files
    """
    if queryset.exists():
        data_frame = pd.DataFrame(queryset.values(*fields))

        for image_path in data_frame['image']:
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            shutil.copy(full_image_path, settings.BASE_DATASET_IMAGE_PATH)

        data_frame['image'] = data_frame['image'].apply(lambda x: x.split('/')[-1])

        data_frame.to_csv(csv_path, index=False)
        print(f'Saved path: {csv_path}')
    else:
        print(f'No records to create the file {csv_path}')


def import_base_dataset(model: Union[Training, TrainingElement], csv_path: str) -> None:
    """
    Reads a CSV file to create model instances with associated image files, and performs a bulk save to the database.
    """
    data_frame = pd.read_csv(csv_path)
    to_create = []

    for index, row in data_frame.iterrows():
        image_path = Path(settings.BASE_DATASET_IMAGE_PATH) / row['image']
        image_file = File(open(image_path, 'rb'))

        instance_data = {key: value for key, value in row.items() if key != 'image'}
        instance_data['image'] = image_file

        to_create.append(model(**instance_data))
    model.objects.bulk_create(to_create)

    print(f'Successful import of objects: {csv_path}')
