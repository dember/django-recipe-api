from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)

        if ingredients:
            for ingredient in ingredients:
                Ingredient.objects.create(**ingredient, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)

        super(RecipeSerializer, self).update(instance, validated_data)

        Ingredient.objects.filter(recipe=instance).delete()

        if ingredients:
            for ingredient in ingredients:
                Ingredient.objects.create(**ingredient, recipe=instance)

        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
