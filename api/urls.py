from django.urls import path

from .views import (
    FavoriteView,
    FollowView,
    PurchaseView,
    ingredients
)


urlpatterns = [
    path(
        "favorites/",
        FavoriteView.as_view(),
        name='favorite_add'
    ),
    path(
        'favorites/<int:pk>/',
        FavoriteView.as_view(),
        name='favorite_remove'
    ),
    path(
        "subscriptions/",
        FollowView.as_view(),
    ),
    path(
        "subscriptions/<int:pk>/",
        FollowView.as_view(),
    ),
    path(
        'purchases/',
        PurchaseView.as_view(),
        name='purchase_add'
    ),
    path(
        'purchases/<int:pk>/',
        PurchaseView.as_view(),
        name='purchase_remove'
    ),
    path(
        'ingredients/',
        ingredients,
        name="ingredients"
    )

]
