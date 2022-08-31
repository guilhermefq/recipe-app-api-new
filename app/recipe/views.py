"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDetailSerializer

    # to filter the queryset, and find the recipes that belong to the user
    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-created_at')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """View for manage tag APIs"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """View for manage ingredients APIs"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
