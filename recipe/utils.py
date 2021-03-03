from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from collections import Counter

from .models import *


def pagination(request, data, count_item):
    """
    Метод формирующий пагинацию.
    """

    paginator = Paginator(
        data,
        count_item
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return paginator, page


def get_ingredients(request):
    """
    Метод формирующий словарь ингредиентов,
    для формы создания рецептов.
    """

    ingredients = {}
    for key, title in request.POST.items():
        if 'nameIngredient' in key:
            elem = key.split("_")
            ingredients[title] = int(
                request.POST[f'valueIngredient_{elem[1]}'])
    return ingredients


def get_cart(request):
    """
    Метод для получения списка покупок.
    Возвращает сумму добавленных продуктов,
    в формате .txt .
    """

    cart_list = Recipe.objects.filter(
        Cart__user=request.user
    ).all()

    ingredients = RecipeIngredient.objects.filter(
        recipe__in=cart_list
    )

    ingredient_list = [
        {i.ingredient: i.quantity} for i in ingredients
    ]

    ingredient_sum = Counter()
    for item in ingredient_list:
        ingredient_sum.update(item)

    finish = [
        (str(i) + " - " + str(k) + '\n')
        for (i, k) in ingredient_sum.items()
    ]

    filename = "recipe_list"
    content = " ".join(finish)
    response = HttpResponse(
        content,
        content_type='text/plain'
    )

    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=500
    )
