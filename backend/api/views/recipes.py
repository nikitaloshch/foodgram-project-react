from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)

from ..filters import IngredientSearchFilter, RecipeFilter
from ..mixins import CreateDestroyViewSet
from ..permissions import AuthorOrReadOnly
from ..serializers.recipes import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeGETSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from ..utils import create_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет создания обьектов класса Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет создания обьектов класса Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientSearchFilter
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет создания обьектов класса Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Позволяет пользователю загрузить список покупок."""
        ingredients_cart = (
            IngredientAmount.objects.filter(
                recipe__shopping_cart__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name'
            ).annotate(ingredient_value=Sum('amount'))
        )
        return create_shopping_cart(ingredients_cart)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeSerializer


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет удаления и добавления рецепта из|в избранного"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["recipe_id"] = self.kwargs.get("recipe_id")
        return context

    def perform_create(self, serializer):
        """Добавление рецепта в избранное"""
        serializer.save(
            user=self.request.user,
            favorite_recipe=get_object_or_404(
                Recipe, id=self.kwargs.get("recipe_id")
            ),
        )

    @action(methods=("delete",), detail=True)
    def delete(self, request, recipe_id):
        """Удаление рецепта из избранного"""
        get_object_or_404(
            Favorite, user=request.user, favorite_recipe_id=recipe_id
        ).delete()
        return Response(
            "Рецепт удален из избранного", status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления и удаления рецепта в/из списка покупок"""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["recipe_id"] = self.kwargs.get("recipe_id")
        return context

    def perform_create(self, serializer):
        """Добавление рецепта в корзину"""
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get("recipe_id")),
        )

    @action(methods=("delete",), detail=True)
    def delete(self, request, recipe_id):
        """Удаление рецепта из корзины"""
        get_object_or_404(
            ShoppingCart, user=request.user, recipe_id=recipe_id
        ).delete()
        return Response(
            "Рецепт удален из корзины", status=status.HTTP_204_NO_CONTENT
        )
