from django.core.management.base import BaseCommand

from apps.data.services.training import duplicate_removal


class Command(BaseCommand):
    def handle(self, *args, **options):
        duplicate_removal()
