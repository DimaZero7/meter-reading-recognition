from django.core.management.base import BaseCommand

from apps.data.services.training import import_training_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_training_data()
