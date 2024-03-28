from django.core.management.base import BaseCommand

from apps.number_reading.models import TrainingSet
from apps.number_reading.services import image_resize


class Command(BaseCommand):
    def handle(self, *args, **options):
        training_set = TrainingSet.objects.all().only("image", "image_resized")
        for training in training_set:
            training.image_resized.delete()
            image_resized_name, image_resized_file = image_resize(
                image=training.image, width=150, height=50
            )
            training.image_resized.save(image_resized_name, image_resized_file)
