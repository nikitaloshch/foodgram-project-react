from django.contrib.admin import ModelAdmin, register

from backend.settings import LIST_PER_PAGE

from .models import Subscription, User


@register(User)
class UserAdmin(ModelAdmin):
    """Класс настройки пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_admin'
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('is_admin',)
    list_filter = ('username', 'email')
    list_per_page = LIST_PER_PAGE
    search_fields = ('username',)


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    """Класс настройки подписок."""

    list_display = (
        'pk',
        'author',
        'subscriber',
    )

    list_editable = ('author', 'subscriber')
    list_filter = ('author',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('author',)
