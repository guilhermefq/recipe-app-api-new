"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

app_name = 'recipe'  # for namespacing, so that we can use reverse()

urlpatterns = [
    # include takes the url patterns generate from the router
    path('', include(router.urls)),
]
