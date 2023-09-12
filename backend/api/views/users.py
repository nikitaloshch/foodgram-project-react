from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from users.models import Subscription, User

from ..mixins import ListSubscriptionViewSet
from ..permissions import AnonimOrAuthenticatedReadOnly
from ..serializers.users import (
    CustomUserSerializer,
    SubscriptionSerializer,
    SubscriptionShowSerializer
)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для создания обьектов класса User."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AnonimOrAuthenticatedReadOnly,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def get_subscribe(self, request, id):
        """Позволяет пользователю подписываться|отписываться от
        от автора контента"""
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={'subscriber': request.user.id, 'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = SubscriptionShowSerializer(
                author, context={'request': request}
            )
            return Response(
                author_serializer.data, status=status.HTTP_201_CREATED
            )
        subscription = get_object_or_404(
            Subscription, subscriber=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetSubscriptions(ListSubscriptionViewSet):
    """Представление списка подписок текущего пользователя"""

    pagination_class = PageNumberPagination
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(subscription__user=self.request.user)
