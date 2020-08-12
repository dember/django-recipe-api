from rest_framework import viewsets

from core.models import Recipe, Ingredient

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name')

        if name:
            return queryset.filter(name__contains=name)

        return Recipe.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
