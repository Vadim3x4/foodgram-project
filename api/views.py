from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import (
    JsonResponse,
    HttpResponse
)


from .models import (
    Favorites_recipe,
    Follow,
    Cart
)
from recipe.models import (
    Recipe,
    User,
    Ingredient
)


class FavoriteView(APIView):
    """
    Класс осуществляющий работу избранных рецептов.
    POST запросы отвечают за добавление рецепта.
    DELETE запросы отвечают за удаление рецепта.
    """

    def post(self, request):
        recipe = get_object_or_404(
            Recipe,
            id=request.data.get('id')
        )
        favorite_obj = Favorites_recipe.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if favorite_obj:
            return Response({'status': '201'})
        return Response({"status": '302'})

    def delete(self, request, pk):
        recipe = get_object_or_404(
            Recipe,
            id=pk
        )
        favorite_obj = get_object_or_404(
            Favorites_recipe,
            user=request.user,
            recipe=recipe
        )
        favorite_obj.delete()
        return Response(
            {"status": '204'}
        )


class FollowView(APIView):
    """
    Класс осуществляющий работу подписок на авторов.
    POST запросы отвечают за добавление автора.
    DELETE запросы отвечают за удаление автора.
    """

    def post(self, request):
        following = get_object_or_404(
            User,
            id=request.data.get('id')
        )
        follow_obj = Follow.objects.get_or_create(
            user=request.user,
            author=following
        )
        if follow_obj:
            return Response(
                {'status': '201'}
            )
        return Response(
            {"status": '302'}
        )

    def delete(self, request, pk):
        following = get_object_or_404(
            User,
            id=pk
        )
        subscribe = get_object_or_404(
            Follow,
            user=request.user,
            author=following
        )
        subscribe.delete()
        return Response(
            {"status": '204'}
        )


class PurchaseView(APIView):
    """
    Класс осуществляющий работу списка товаров.
    POST запросы отвечают за добавление товаров.
    DELETE запросы отвечают за удаление товаров.
    """

    def post(self, request):
        recipe = get_object_or_404(
            Recipe,
            id=request.data.get('id')
        )
        cart_object = Cart.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if cart_object:
            return Response({'status': '201'})
        return Response({"status": '302'})

    def delete(self, request, pk):
        recipe = get_object_or_404(
            Recipe,
            id=pk
        )
        purchase = get_object_or_404(
            Cart,
            user=request.user,
            recipe=recipe
        )
        purchase.delete()
        return Response(
            {"status": '204'}
        )


@login_required
def ingredients(request):
    """
    Метод получения списка ингредиентов,
    для выпадающего списка в форме добавления,
    редактирования рецепта.
    """

    query = str(
        request.GET.get("search")
    ).lower()

    ingredients = Ingredient.objects.filter(
        title__contains=query
    ).values(
        "title",
        "dimension"
    )

    return JsonResponse(list(ingredients), safe=False)
