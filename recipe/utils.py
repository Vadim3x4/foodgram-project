from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum

from api.models import Cart
from models import *

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

    cart = Cart.objects.filter(user=request.user)
    ingredients = cart.values(
        'recipe__ingredients__title',
        'recipe__ingredients__dimension'
    ).annotate(
        total_quantity=Sum(
            'recipe__recipeingredient__quantity'
        )
    )

    content = ""
    for ingredient in ingredients:
        item = (f'{ingredient["recipe__ingredients__title"]} '
                f'{ingredient["total_quantity"]} '
                f'{ingredient["recipe__ingredients__dimension"]}')
        content += item + '\n'

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=recipe_list'
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
