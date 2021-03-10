from django.urls import path

from .views import (
    AboutPage,
    TechPage
)


urlpatterns = [
    path(
        'about_page/',
        AboutPage.as_view(),
        name='AboutPage'
    ),
    path(
        'tech_page/',
        TechPage.as_view(),
        name='TechPage'
    )
]
