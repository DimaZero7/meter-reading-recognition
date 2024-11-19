import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.data.models import Training, TrainingElement
from apps.data.choices import TrainingType
from apps.data.services.base_data import import_base_dataset


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_base_dataset(
            model=Training, csv_path=settings.BASE_DATASET_TRAINING_CSV_PATH
        )
        import_base_dataset(
            model=TrainingElement, csv_path=settings.BASE_DATASET_TRAINING_ELEMENT_CSV_PATH
        )
