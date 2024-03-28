import os
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand

from apps.number_reading.models import TrainingSet


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_path = os.path.join(
            Path(__file__).resolve().parent.parent.parent.parent.parent, "data_csv", "training_set"
        )
        files = os.listdir(data_path)

        for file_name in files:
            data = pd.read_csv(os.path.join(data_path, file_name))

            training_samples = []
            for index, row in data.iterrows():
                training_sample = TrainingSet(
                    image=row["image"],
                    type=row["type"],
                    correct_value=float(row["correct_value"]),
                )
                training_samples.append(training_sample)

            TrainingSet.objects.bulk_create(training_samples)
