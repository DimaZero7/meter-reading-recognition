from django.urls import path

from services.api.web.training_set.views import TrainingSetCreateView

app_name = "training_set"

urlpatterns = [
    path("create/", TrainingSetCreateView.as_view(), name="create"),
]
