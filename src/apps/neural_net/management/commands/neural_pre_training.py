from django.core.management.base import BaseCommand

from apps.data.services.data_preparation import DataPreparation
from apps.neural_net.services.layers import ModelManager


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)
        parser.add_argument('epochs', type=int)
        parser.add_argument('changes', type=str)

    def handle(self, *args, **options):
        model_name = options['model_name']
        epochs = options['epochs']
        changes = options['changes']

        training_generator, test_generator, validation_generator = DataPreparation().get_image_generators()
        model = ModelManager(model_name=model_name)
        model.start_training(training_generator=training_generator, test_generator=test_generator, epochs=epochs)
        model.save(model_name=model_name, validation_generator=validation_generator, changes=changes)
