from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', views.CustomUserViewSet, basename='users')
router.register('subscriptions', views.SubscriptionViewSet,
                basename='subscriptions')
router.register('tags', views.TagViewSet, basename='tags')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('shopping_cart', views.ShoppingCartViewSet,
                basename='shopping_cart')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
