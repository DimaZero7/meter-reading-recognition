from django.core.management.base import BaseCommand

from apps.data.services.augmentation_data import CreateAugmentationData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('training_element_type', type=int)
        parser.add_argument('number_images', type=int)

    def handle(self, *args, **options):
        training_element_type = options['training_element_type']
        number_images = options['number_images']

        CreateAugmentationData().generate_augmentations(augmentation_type=training_element_type, number_images=number_images)
