from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404
)


from .forms import RecipeForm
from api.models import Favorites_recipe
from .models import (
    User,
    Recipe
)
from .utils import (
    pagination,
    get_ingredients
)


def index(request):
    """
    Метод для вывода данных, 
    главной страницы.
    """

    tags = request.GET.getlist('tag')
    recipe_list = Recipe.objects.tag_filter(tags)
    paginator, page = pagination(
        request,
        recipe_list,
        5
    )
    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': True
        }
    )


def recipe_card(request, recipe_id):
    """
    Метод для вывода данных, 
    персональной карточки рецепта.
    """

    recipe_card = get_object_or_404(
        Recipe,
        id=recipe_id
    )
    return render(
        request,
        "recipe/recipe_card.html",
        {
            "recipe_card": recipe_card,
        }
    )


@login_required
def recipe_favorites(request):
    """
    Метод для вывода данных, 
    избранных рецептов.
    """

    tags = request.GET.getlist('tag')
    favorite_list = Favorites_recipe.objects.favorite_recipe(
        request.user,
        tags
    )
    paginator, page = pagination(
        request,
        favorite_list,
        3
    )
    return render(
        request,
        "recipe/favorites_recipes.html",
        {
            'page': page,
            'paginator': paginator,
            'title': 'Избранное',
            'tags': True
        }
    )


def recipe_author(request, author_id):
    """
    Метод для вывода данных списка покупок.
    """

    tags = request.GET.getlist('tag')
    author = get_object_or_404(
        User,
        id=author_id
    )
    author_recipes = Recipe.objects.tag_filter(
        tags
    ).filter(
        author=author
    )
    paginator, page = pagination(
        request,
        author_recipes,
        3
    )
    return render(
        request,
        "recipe/author_recipes.html",
        {
            'page': page,
            'paginator': paginator,
            'title': author,
            'tags': True
        }
    )


@login_required
def recipe_cart(request):
    """
    Метод для вывода данных, для списка покупок.
    """

    cart_list = Recipe.objects.filter(
        Cart__user=request.user
    )
    return render(
        request,
        "recipe/cart.html",
        {
            'cart_list': cart_list
        }
    )


@login_required
def recipe_add(request):
    """
    Метод cоздания нового рецепта.
    """

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    print(form)
    context = {'form': form}
    if request.method != 'POST':
        return render(
            request,
            'recipe/add_recipe.html',
            context
        )
    else:
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            ingredients = get_ingredients(request)
            for title, quantity in ingredients.items():
                ingredient = get_object_or_404(
                    Ingredient,
                    title=title
                )
                recipe_ing = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )
                recipe_ing.save()
            return redirect('index')
    return render(
        request,
        'recipe/add_recipe.html',
        {
            'form': form
        }
    )


@login_required
def recipe_edit(request, recipe_id):
    """
    Метод для редактирования рецепта.
    """

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )
    author = recipe.author
    if author != request.user:
        return redirect('index')
    else:
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                ingredients = get_ingredients(request)
                for title, quantity in ingredients.items():
                    ingredient = get_object_or_404(
                        Ingredient,
                        title=title
                    )
                    recipe_ing = RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=quantity
                    )
                    recipe_ing.save()

            return redirect('index')
        return render(
            request,
            'recipe/add_recipe.html',
            {
                'form': form,
                'recipe': recipe
            }
        )


@login_required
def recipe_delete(request, recipe_id):
    """
    Метод для удаления рецепта.
    """

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )
    author = recipe.author
    if author != request.user:
        return redirect('index')
    else:
        recipe.delete()
    return redirect('index')


@login_required
def my_follow(request):
    """
    Метод для вывода данных, подписок на выбранных авторов.
    """

    author_list = User.objects.prefetch_related(
        'recipe_author'
    ).filter(
        following__user=request.user)
    paginator, page = pagination(
        request,
        author_list,
        3
    )
    return render(
        request,
        "recipe/my_follow.html",
        {
            'page': page,
            'paginator': paginator,
            'title': 'Мои подписки',
        }
    )
