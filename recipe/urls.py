from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .utils import (
    get_cart,
    page_not_found,
    server_error
)


urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        '404/',
        page_not_found,
        name='404'
    ),
    path(
        '500/',
        server_error,
        name='404'
    ),
    path(
        'recipe/<int:recipe_id>',
        views.recipe_card,
        name='recipe_card'
    ),
    path(
        'recipe_favorites/',
        views.recipe_favorites,
        name='favorites'
    ),
    path(
        'my_follow/',
        views.my_follow,
        name='my_follow'
    ),
    path(
        'recipe_author/<int:author_id>',
        views.recipe_author,
        name='recipe_author'
    ),
    path(
        'recipe_add/',
        views.recipe_add,
        name='recipe_add'
    ),
    path(
        'recipe_edit/<int:recipe_id>',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'recipe_cart/',
        views.recipe_cart,
        name='cart'
    ),
    path(
        'get_cart/',
        get_cart,
        name='get_cart'
    ),
    path(
        'recipe_delete/<int:recipe_id>/',
        views.recipe_delete,
        name='recipe_delete'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

