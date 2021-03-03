from django.contrib import admin
from .models import *


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'dimension'
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
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
        'time',
        'text',
        'pub_date',
        'author',
        'image',
    )
    list_filter = (
        'title',
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
