"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    tags = TagSerializer(
        many=True, required=False)
    # many=True means many tags can be assigned to a recipe
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price',
                  'link', 'tags', 'ingredients', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def _get_or_create_tags(self, tags, recipe):
        """Create and return tags"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    # starts with _ mean that this function is internal to the class
    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed"""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create and return a new recipe"""
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags_data, recipe)
        self._get_or_create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
