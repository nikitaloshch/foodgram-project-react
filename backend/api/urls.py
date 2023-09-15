from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', views.users.CustomUserViewSet, basename='users')
router.register('subscriptions', views.users.SubscriptionViewSet,
                basename='subscriptions')
router.register('tags', views.recipes.TagViewSet, basename='tags')
router.register('ingredients', views.recipes.IngredientViewSet,
                basename='ingredients')
router.register('recipes', views.recipes.RecipeViewSet, basename='recipes')
router.register('shopping_cart', views.recipes.ShoppingCartViewSet,
                basename='shopping_cart')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
