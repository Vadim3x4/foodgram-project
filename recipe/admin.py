from django.contrib import admin
from django.db.models import Count

from .models import (
    Ingredient,
    RecipeIngredient,
    Recipe,
    RecipeTags,
    Tag
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeTagInline(admin.TabularInline):
    model = RecipeTags
    extra = 1



@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'dimension'
    )
    search_fields = (
        'title',
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'quantity'
    )
    search_fields = (
        'ingredient',
        'quantity'
    )
    list_filter = (
        'ingredient',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        RecipeIngredientInline,
        RecipeTagInline
    )
    list_display = (
        'title',
        'author',
        'get_favorite',
    )
    search_fields = (
        'title',
        'author',
        'tags',
    )
    list_filter = (
        'author',
        'title',
        'tags'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            added_favorite=Count('favorites_recipe')
        )

    def get_favorite(self, obj):
        return obj.added_favorite

    get_favorite.short_description = 'добавлен в избранное, раз'


@admin.register(RecipeTags)
class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'tag'
    )


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'color'
    )
