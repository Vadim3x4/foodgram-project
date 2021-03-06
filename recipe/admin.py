from django.contrib import admin

from .models import *


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
    list_display = (
        'title',
        'author',
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

