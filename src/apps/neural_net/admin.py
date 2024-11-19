from django.contrib import admin

from .models import NeuralModel, NeuralVersion
from ..common.admin import SearchHelpTextMixin


@admin.register(NeuralModel)
class TrainingAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display

    search_fields = ('id', 'name',)

    list_per_page = 50


@admin.register(NeuralVersion)
class NeuralVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'neural_model', 'version')
    list_display_links = list_display

    search_fields = ('version', 'changes')
    list_per_page = 50
