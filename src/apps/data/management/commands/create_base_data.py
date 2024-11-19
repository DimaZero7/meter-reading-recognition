from django.conf import settings
from django.core.management.base import BaseCommand

from apps.data.choices import TrainingType
from apps.data.models import Training, TrainingElement
from apps.data.services.base_data import create_base_dataset


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_base_dataset(
            queryset=Training.objects.filter(type__in=[TrainingType.TEST.value, TrainingType.VALIDATE.value]),
            fields=['image', 'type', 'correct_value'],
            csv_path=settings.BASE_DATASET_TRAINING_CSV_PATH
        )
        create_base_dataset(
            queryset=TrainingElement.objects.all(),
            fields=['image', 'number_type', 'type', 'correct_value'],
            csv_path=settings.BASE_DATASET_TRAINING_ELEMENT_CSV_PATH
        )
