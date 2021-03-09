from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import (
    JsonResponse,
    HttpResponse
)


from .models import (
    FavoritesRecipe,
    Follow,
    Cart
)
from recipe.models import (
    Recipe,
    User,
    Ingredient
)


class FavoriteView(LoginRequiredMixin, APIView):
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
        favorite_obj = FavoritesRecipe.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if favorite_obj:
            return JsonResponse(
                {'status': '201'}
            )
        return JsonResponse(
            {"status": '302'}
        )

    def delete(self, request, pk):
        del_like = FavoritesRecipe.objects.filter(
            user=request.user,
            recipe_id=pk
        ).delete()
        if del_like is 0:
            return JsonResponse(
                {"status": '404'}
            )
        return JsonResponse(
            {"status": '204'}
        )


class FollowView(LoginRequiredMixin, APIView):
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
            return JsonResponse(
                {'status': '201'}
            )
        return JsonResponse(
            {"status": '302'}
        )

    def delete(self, request, pk):
        del_follow = Follow.objects.filter(
            user=request.user,
            author_id=pk
        ).delete()
        if del_follow is 0:
            return JsonResponse(
                {"status": '404'}
            )
        return JsonResponse(
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
            return JsonResponse(
                {'status': '201'}
            )
        return JsonResponse(
            {"status": '302'}
        )

    def delete(self, request, pk):
        del_follow = Cart.objects.filter(
            user=request.user,
            recipe_id=pk
        ).delete()
        if del_follow is 0:
            return JsonResponse(
                {"status": '404'}
            )
        return JsonResponse(
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
