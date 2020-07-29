from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, related_name='ingredients')

    def __str__(self):
        return self.name
