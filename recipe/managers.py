from django.db import models


class RecipeManager(models.Manager):

    @staticmethod
    def tag_filter(tags):
        from .models import Recipe
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).order_by(
                '-pub_date').distinct()
        else:
            return Recipe.objects.order_by('-pub_date').all()


class FavoriteRecipeManager(models.Manager):

    @staticmethod
    def favorite_recipe(user, tags):
        from api.models import FavoritesRecipe
        from .models import Recipe
        favorite = FavoritesRecipe.objects.filter(
            user=user
        ).all()
        recipes_id = favorite.values_list(
            'recipe',
            flat=True
        )
        favorite_list = Recipe.objects.tag_filter(
            tags
        ).filter(
            pk__in=recipes_id
        ).order_by('-pub_date')
        return favorite_list
