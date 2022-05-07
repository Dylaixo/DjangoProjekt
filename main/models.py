from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=f'attractions_images/', blank=True)

    def __str__(self):
        return self.name


class Attractions(models.Model):
    name = models.CharField(max_length=200)
    time = models.PositiveSmallIntegerField(help_text="czas podany w minutach")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'attractions_images/', blank=True)
    desc = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    attractions = models.ManyToManyField(Attractions, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField()
