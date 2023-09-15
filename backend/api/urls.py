from django.urls import include, path
from rest_framework import routers

from .views.users import CustomUserViewSet, SubscriptionViewSet
from .views.recipes import (
    TagViewSet,
    ShoppingCartViewSet,
    RecipeViewSet,
    IngredientViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('subscriptions', SubscriptionViewSet,
                basename='subscriptions')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet,
                basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('shopping_cart', ShoppingCartViewSet,
                basename='shopping_cart')


urlpatterns = [
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionViewSet.as_view(),
        name='subscribe'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        CustomUserViewSet.as_view(),
        name='favorite_recipe'),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartViewSet.as_view(),
        name='shopping_cart'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
