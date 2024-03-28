from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from rangefilter.filters import NumericRangeFilter

from apps.number_reading.models import TrainingSet


@admin.register(TrainingSet)
class TrainingSetAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "correct_value", "get_image")
    list_display_links = list_display

    list_per_page = 10
    list_filter = (("id", NumericRangeFilter), "type", ("correct_value", NumericRangeFilter))

    fields = ("image", "image_resized", "correct_value", "type", "correct_value_categorical")
    readonly_fields = ("type", "correct_value_categorical", "image_resized")

    def get_image(self, instance: TrainingSet):
        return mark_safe(
            f'<img src="{settings.DOMAIN_NAME}{instance.image.url}" '
            f'class="admin-icon" width="100">'
        )

    # def has_delete_permission(self, request, obj=None):
    #     return False
