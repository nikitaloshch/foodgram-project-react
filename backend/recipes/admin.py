from django.contrib.admin import ModelAdmin, TabularInline, register

from backend.settings import LIST_PER_PAGE

from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)


@register(Tag)
class TagAdmin(ModelAdmin):
    """Класс настройки раздела тегов."""

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """Класс настройки раздела ингредиентов."""

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)


class IngredientAmountInline(TabularInline):
    """Класс, позволяющий добавлять ингредиенты в рецепты."""

    model = IngredientAmount
    min_num = 1


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """Класс настройки раздела рецептов."""

    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        IngredientAmountInline,
    ]

    empty_value_display = 'значение отсутствует'
    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author', 'name')

    def get_ingredients(self, object):
        """Получает ингредиент или список ингредиентов рецепта."""
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    get_ingredients.short_description = 'ингредиенты'

    def get_tags(self, object):
        """Получает тег или список тегов рецепта."""
        return '\n'.join((tag.name for tag in object.tags.all()))

    get_tags.short_description = 'теги'

    def count_favorite(self, object):
        """Вычисляет количество добавлений рецепта в избранное."""
        return object.favoriting.count()

    count_favorite.short_description = 'Количество добавлений в избранное'


@register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    """Класс настройки соответствия игредиентов и рецептов."""

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )
    empty_value_display = 'значение отсутствует'
    list_per_page = LIST_PER_PAGE


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    """Класс настройки раздела избранного."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = LIST_PER_PAGE


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    """Класс настройки раздела рецептов, которые добавлены в список покупок."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = LIST_PER_PAGE
