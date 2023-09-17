from django.urls import include, path
from rest_framework import routers

from .views.recipes import (IngredientViewSet, RecipeViewSet,
                            TagViewSet, ShoppingCartViewSet)
from .views.users import CustomUserViewSet, SubscriptionViewSet

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register(r'subscriptions', SubscriptionViewSet,
                basename='subscriptions')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', CustomUserViewSet.as_view(
        {'get': 'get_subscriptions'}), name='get-subscriptions'),
    path('users/<int:pk>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'subscribe',
                                      'delete': 'unsubscribe'}),
         name='subscribe-unsubscribe'),
    path('recipes/<int:pk>/favorite/',
         RecipeViewSet.as_view({'post': 'get_favorite',
                                'delete': 'get_favorite'}),
         name='add_favorite-remove_favorite'),
    path('recipes/<int:pk>/shopping_cart/',
         RecipeViewSet.as_view({'post': 'get_shopping_cart',
                                'delete': 'get_shopping_cart'}),
         name='add_shopping_cart-remove_shopping_cart'),
    path('recipes/download_shopping_cart/', ShoppingCartViewSet.as_view(
        {'get': 'download_shopping_cart'}), name='download_shopping_cart'),
    path('', include(router.urls)),
]
