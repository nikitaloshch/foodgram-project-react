from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Класс для ViewSet Избранного и Списка покупок"""


class ListSubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Класс для представления списка подписок"""