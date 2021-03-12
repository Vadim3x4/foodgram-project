from django import template


from api.models import Follow, FavoritesRecipe, Cart
from recipe.models import Tag

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_subscribe(value, user):
    """
    Фильтрует запросы связанные,
    с добавление объекта подписки.
    """
    return Follow.objects.filter(
        author=value,
        user=user
    ).exists()


@register.filter
def is_favorite(value, user):
    """
    Фильтрует запросы связанные,
    с добавление объекта в избранное.
    """
    return FavoritesRecipe.objects.filter(
        recipe=value,
        user=user
    ).exists()


@register.filter
def is_purchase(request, recipe):
    """
    Фильтровать набор запросов,
    c добавление объекта в список покупок.
    """
    return Cart.objects.filter(
        user=request.user,
        recipe=recipe
    )


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def get_active_tags(value):
    return value.getlist('tag')


@register.filter
def change_tag_link(request, tag):
    copy = request.GET.copy()
    if copy.getlist('page'):
        copy.pop('page')
    tag_link = copy.getlist('tag')
    if tag.slug in tag_link:
        tag_link.remove(tag.slug)
        copy.setlist('tag', tag_link)
    else:
        copy.appendlist('tag', tag.slug)
    return copy.urlencode()


@register.filter
def get_count_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).count()



@register.filter
def get_count_recipes(recipe):
    count_recipe = len(recipe) - 3
    if count_recipe < 1:
        return False

    if count_recipe % 10 == 1 and count_recipe % 100 != 11:
        end = 'рецепт'
    elif 2 <= count_recipe % 10 <= 4 and (count_recipe % 100 < 10 or count_recipe % 100 >= 20):
        end = 'рецепта'
    end = 'рецептов'

    return f'Еще {count_recipe} {end}...'