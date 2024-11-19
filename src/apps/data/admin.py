from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Training, TrainingElement, TrainingAugmentation
from ..common.admin import SearchHelpTextMixin


@admin.register(Training)
class TrainingAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    list_display = ('id', 'type', 'correct_value', 'get_image')
    list_display_links = list_display

    list_filter = ('type',)
    search_fields = ('id', 'correct_value',)

    list_per_page = 50

    def get_image(self, instance: Training):
        return mark_safe(
            f'<img src="{settings.DOMAIN_NAME}{instance.image.url}" '
            f'class="admin-icon" width="{settings.IMAGE_SIZE_X}" height="{settings.IMAGE_SIZE_Y}">'
        )


@admin.register(TrainingElement)
class TrainingElementAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    list_display = ('id', 'number_type', 'meter_type', 'correct_value', 'get_image')
    list_display_links = list_display

    list_filter = ('meter_type', 'number_type')
    search_fields = ('id', 'correct_value',)

    list_per_page = 50

    def get_image(self, instance: TrainingElement):
        return mark_safe(
            f'<img src="{settings.DOMAIN_NAME}{instance.image.url}" '
            f'class="admin-icon">'
        )


@admin.register(TrainingAugmentation)
class TrainingSetAugmentationAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    list_display = ('id', 'meter_type', 'correct_value', 'get_image')
    list_display_links = list_display

    list_filter = ('meter_type', 'type')
    search_fields = ('id', 'correct_value',)

    list_per_page = 50

    def get_image(self, instance: TrainingAugmentation):
        return mark_safe(
            f'<img src="{settings.DOMAIN_NAME}{instance.image.url}" '
            f'class="admin-icon" width="{settings.IMAGE_SIZE_X}" height="{settings.IMAGE_SIZE_Y}">'
        )
