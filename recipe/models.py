from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class RecipeManager(models.Manager):

    @staticmethod
    def tag_filter(tags):
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).order_by(
                '-pub_date').distinct()
        else:
            return Recipe.objects.order_by('-pub_date').all()


class Tag(models.Model):
    """
    Модель для тэгов фильтрации.
    """
    title = models.CharField(
        max_length=50
    )
    color = models.CharField(
        max_length=50
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """
    Модель для фиксации единиц измерения,
    каждого ингредиента в базе.
    """

    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента'
    )
    dimension = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.title} ({self.dimension})'


class Recipe(models.Model):
    """
    Модель определящая рецепт.
    """

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    time = models.PositiveIntegerField(
        null=False,
        verbose_name='Время приготовления'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание рецепта'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe_author'
    )
    image = models.ImageField(
        upload_to='recipe/',
        null=False,
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        through='RecipeTags',
        related_name='tags',
        verbose_name='Тэги'
    )

    objects = RecipeManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class RecipeTags(models.Model):
    """
    Модель определящая тэги,
    использующиеся для фильтрации рецептов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
        related_name='recipetag'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Название тэга',
        related_name='recipetag'
    )

    class Meta:
        verbose_name = "Тэги рецепта"
        verbose_name_plural = "Тэги рецепта"
        unique_together = (
            'recipe',
            'tag'
        )


class RecipeIngredient(models.Model):
    """
    Модель для фиксации наименования и
    колличества инредиентов у выбранных рецептов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
        related_name='recipeingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Название ингредиента',
        related_name='recipe_ingredient'

    )
    quantity = models.PositiveIntegerField(
        verbose_name='Колличество ингредиентов'
    )

    class Meta:
        verbose_name_plural = "Ингредиенты для рецепта"

    def __str__(self):
        return f'{self.ingredient} - {self.quantity}'
