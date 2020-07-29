from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
