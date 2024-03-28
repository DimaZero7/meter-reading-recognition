from django.core.management.base import BaseCommand

from apps.number_reading.models import TrainingSet
from apps.number_reading.services import convert_float_to_categorical


class Command(BaseCommand):
    def handle(self, *args, **options):
        training_set = TrainingSet.objects.all().only("correct_value")
        updated_trainings = []

        for training in training_set:
            training.correct_value_categorical = convert_float_to_categorical(
                number=training.correct_value
            ).tolist()
            updated_trainings.append(training)

        TrainingSet.objects.bulk_update(updated_trainings, ["correct_value_categorical"])
