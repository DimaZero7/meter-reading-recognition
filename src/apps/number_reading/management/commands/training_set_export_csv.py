import os
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand

from apps.number_reading.models import TrainingSet


class Command(BaseCommand):
    def handle(self, *args, **options):
        training_ids = TrainingSet.objects.all().values_list("id", flat=True)
        training_count = len(training_ids)

        chunk_size = 200
        chunk_count = training_count // chunk_size + 1

        data_path = os.path.join(
            Path(__file__).resolve().parent.parent.parent.parent.parent, "data_csv", "training_set"
        )

        files_name = list(map(int, os.listdir(data_path)))
        shift_number = max(files_name) if files_name else 0

        for chunk_number in range(chunk_count):
            start_index = chunk_number * chunk_size
            end_index = min((chunk_number + 1) * chunk_size, training_count)

            chunk_training_ids = training_ids[start_index:end_index]
            chunk_trainings = TrainingSet.objects.filter(id__in=chunk_training_ids)

            images = list(chunk_trainings.values_list("image", flat=True))
            types = list(chunk_trainings.values_list("type", flat=True))
            correct_values = list(chunk_trainings.values_list("correct_value", flat=True))

            data = pd.DataFrame(
                {
                    "image": images,
                    "type": types,
                    "correct_value": correct_values,
                }
            )
            data.to_csv(f"{data_path}/{chunk_number + 1 + shift_number}", index=False)
