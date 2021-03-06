from django.contrib.auth import get_user_model
from django.db import models

from recipe.models import Recipe

User = get_user_model()


class FavoriteRecipeManager(models.Manager):

    @staticmethod
    def favorite_recipe(user, tags):
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


class FavoritesRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_recipe"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites_recipe"
    )

    objects = FavoriteRecipeManager()

    class Meta:
        unique_together = (
            'user',
            'recipe'
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscriptions'
            )
        ]

        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписываться на самого себя')


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return self.recipe.title
