from rest_framework.generics import CreateAPIView

from services.api.web.training_set.serializers import TrainingSetCreateSerializer


class TrainingSetCreateView(CreateAPIView):
    permission_classes = ()
    serializer_class = TrainingSetCreateSerializer
