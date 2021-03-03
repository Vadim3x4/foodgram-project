from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500

handler404 = 'recipe.utils.page_not_found'  # noqa
handler500 = 'recipe.utils.server_error'  # noqa


urlpatterns = [
    path(
        "",
        include("recipe.urls")
    ),
    path(
        "auth/",
        include("django.contrib.auth.urls")
    ),
    path(
        "auth/",
        include("users.urls")
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api/',
        include('api.urls')
    ),
    path(
        'static_page/',
        include('site_info.urls')
    ),
]
