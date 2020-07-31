from rest_framework import viewsets

from core.models import Recipe, Ingredient

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)

        return queryset


class IngredientViewSet(viewsets.ModelViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
