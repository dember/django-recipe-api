from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Description of sample recipe'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def sample_ingredient(name='Cinnamon'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(name=name)


class PublicRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {
            'name': 'Chocolate cheesecake',
            'description': 'Description of chocolate cheesecake',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(name='Prawns')
        ingredient2 = sample_ingredient(name='Ginger')
        payload = {
            'name': 'Thai prawn red curry',
            'description': 'Description',
            'ingredients': [ingredient1.id, ingredient2.id],
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_filter_recipes_by_name(self):
        """Test filter recipes by name"""
        ingredient1 = sample_ingredient(name='Prawns')
        ingredient2 = sample_ingredient(name='Ginger')
        payload = {
            'name': 'Thai prawn red curry',
            'description': 'Description',
            'ingredients': [ingredient1.id, ingredient2.id],
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(RECIPES_URL + '?name=Thai')
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_recipes_by_name_with_non_matching_name(self):
        """Test filter recipes by name"""
        ingredient1 = sample_ingredient(name='Prawns')
        ingredient2 = sample_ingredient(name='Ginger')
        payload = {
            'name': 'Thai prawn red curry',
            'description': 'Description',
            'ingredients': [ingredient1.id, ingredient2.id],
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(RECIPES_URL + '?name=X')
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)
